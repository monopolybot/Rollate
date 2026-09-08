import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, CallbackQueryHandler, filters

# بيانات الأسئلة محدثة ومصححة
GAMES_LIST = [
    {
        "id": 3,
        "spoiler_file_id": "AgACAgQAAxkBAAM4aqAOgoSz2xm4ouiLmWr0UAK08i4AAgwQaxuCQ_lQU3f7CtC9CssBAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAAM-aqAQvrNbpcZ7pda2HT6DU7LDy3YAAg0QaxuCQ_lQ9c6BscarZs0BAAMCAAN5AAM9BA",
        "correct_answer": "ميران",
    }
]


active_games = {}
user_scores = {}


def setup_game_handlers(app):
    # هاندلر لبدء لعبة الغباش عند كتابة كلمة "غباش"
    async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.text:
            return
        
        chat_id = update.effective_chat.id
        games = GAMES_LIST
        if not games:
            await update.message.reply_text("❌ عذراً، لا توجد أسئلة مخزنة.")
            return

        if chat_id not in active_games:
            active_games[chat_id] = {"question_index": 0, "winner_found": False}
        else:
            current_idx = active_games[chat_id]["question_index"]
            if current_idx >= len(games):
                active_games[chat_id]["question_index"] = 0

        q_data = games[active_games[chat_id]["question_index"]]
        active_games[chat_id]["winner_found"] = False

        start_msg_text = (
            "👑 **يا اساطير شعب مونوبولي العظيم** 👑\n\n"
            "🔥 **لقد بدأ تحدي الغباش** 🔥\n\n"
            "🧩 **كل ما هو عليك ان تضغط على الصورة ذات الغباش، وتجمع الاحرف مع بعضها لتظهر لنا الكلمة الصحيحة** 🧩"
        )
        await context.bot.send_message(chat_id, start_msg_text, parse_mode="HTML")

        keyboard = [[InlineKeyboardButton("📊 دفتر النتائج", callback_data="show_scoreboard")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            sent_msg = await context.bot.send_photo(
                chat_id=chat_id,
                photo=str(q_data["spoiler_file_id"]),
                reply_markup=reply_markup,
                has_spoiler=True
            )
        except Exception as e:
            print(f"❌ [خطأ تقني في لعبة الغباش - إرسال صورة الغباش]: {e}")
            await update.message.reply_text(f"❌ حدث خطأ أثناء إرسال الصورة: {e}")
            return

        # تشغيل حلقة التشجيع في الخلفية
        asyncio.create_task(encouragement_loop(context, chat_id))

    async def encouragement_loop(context, chat_id):
        elapsed = 0
        while elapsed < 30:
            await asyncio.sleep(5)
            elapsed += 5

            if chat_id in active_games and active_games[chat_id]["winner_found"]:
                break

            encouraging_text = (
                f"⏳ **مضى {elapsed} ثواني على صورة الغباش ولم يتم حل اللغز!** ⏳\n\n"
                "⚡ **اين انتم يا عشاق التحدي؟! استيقظوا واكشفوا الكلمة!** ⚡"
            )
            try:
                await context.bot.send_message(chat_id, encouraging_text, parse_mode="HTML")
            except Exception:
                break

    # هاندلر استقبال الإجابات والرسائل
    async def handle_game_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.text:
            return
        if not update.effective_chat or not update.effective_chat.type in ["group", "supergroup"]:
            return

        chat_id = update.effective_chat.id
        if chat_id not in active_games or active_games[chat_id]["winner_found"]:
            return

        user_text = update.message.text.strip()
        games = GAMES_LIST
        current_idx = active_games[chat_id]["question_index"]
        q_data = games[current_idx]

        if user_text == q_data["correct_answer"]:
            active_games[chat_id]["winner_found"] = True
            user = update.effective_user
            if not user:
                return
            user_id = user.id
            user_name = user.first_name or "المتحدي"

            if chat_id not in user_scores:
                user_scores[chat_id] = {}
            if user_id not in user_scores[chat_id]:
                user_scores[chat_id][user_id] = {"name": user_name, "score": 0}

            user_scores[chat_id][user_id]["score"] += 1
            current_score = user_scores[chat_id][user_id]["score"]

            keyboard = [[InlineKeyboardButton("📊 دفتر النتائج", callback_data="show_scoreboard")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            try:
                await update.message.reply_photo(
                    photo=str(q_data["answer_file_id"]),
                    caption=(
                        "🎉 **مبروووووك يا بطل** 🎉\n\n"
                        "✅ **جوابك صحيح ١٠٠٪** ✅\n\n"
                        "🎯 **استمر في التحدي**"
                    ),
                    parse_mode="HTML",
                    reply_markup=reply_markup,
                )
            except Exception as e:
                print(f"❌ [خطأ تقني في لعبة الغباش - إرسال صورة الجواب]: {e}")

            if current_score >= 5:
                congrats_msg = (
                    f"🏆 **مبروووووك يا اسطورة الغباش <a href='tg://user?id={user_id}'>{user_name}</a>** 🏆\n\n"
                    "🌟 **لقد حققت خمس انتصارات وتغلبت على الجميع!** 🌟"
                )
                await context.bot.send_message(chat_id, congrats_msg, parse_mode="HTML")
                user_scores[chat_id][user_id]["score"] = 0

            active_games[chat_id]["question_index"] += 1

    # هاندلر الأزرار (Callback Query)
    async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        if not query or not query.data:
            return
        
        data = query.data
        chat_id = query.message.chat_id if query.message else None

        if data == "show_scoreboard":
            if not chat_id or chat_id not in user_scores or not user_scores[chat_id]:
                await query.answer("دفتر النتائج فارغ حتى الآن، كن أول الفائزين!", show_alert=True)
                return

            sorted_users = sorted(
                user_scores[chat_id].values(), key=lambda x: x["score"], reverse=True
            )

            score_text = "📊 **--- دفتر النتائج والمراتب ---** 📊\n\n"
            for idx, item in enumerate(sorted_users[:10], start=1):
                score_text += f"🏅 **{idx}. {item['name']}** ⟵ **{item['score']}** انتصارات\n"

            keyboard = [
                [
                    InlineKeyboardButton("◀️ السابق", callback_data="prev_score"),
                    InlineKeyboardButton("التالي ▶️", callback_data="next_score"),
                ],
                [InlineKeyboardButton("❌ إغلاق", callback_data="close_score")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.reply_text(score_text, parse_mode="HTML", reply_markup=reply_markup)
            await query.answer()

        elif data == "close_score":
            try:
                await query.message.delete()
            except Exception:
                pass
            await query.answer()
        elif data in ["prev_score", "next_score"]:
            await query.answer("هذه الصفحة الحالية للنتائج", show_alert=True)

    # تسجيل الهاندلرز في تطبيق python-telegram-bot
    app.add_handler(MessageHandler(filters.Regex("^غباش$"), start_game))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_game_message))
    app.add_handler(CallbackQueryHandler(callback_handler, pattern="^(show_scoreboard|close_score|prev_score|next_score)$"))
