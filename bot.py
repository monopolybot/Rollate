# =========================================================
# bot.py - الكود المحدث بالكامل
# =========================================================

import asyncio
import html
import re
import unicodedata

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)


# =========================================================
# بيانات لعبة الغباش
# =========================================================

GAMES_LIST = [
    {
        "id": 1,
        "spoiler_file_id": "AgACAgQAAxkBAANAaqAqF_AFnQsqGL46Mc6EXE8pqs4AAhMTaxvR7QlR0all_mZvUZgBAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAANCaqAqoQfQaj6HnFROGYai4iwaenUAAgEQaxssGwFRpCeiUPk9mU4BAAMCAAN5AAM9BA",
        "correct_answer": "ميران",
    },
    {
        "id": 2,
        "spoiler_file_id": "AgACAgQAAxkBAANEaqAsv_bh4O4cxXriVWOMW0duMHYAAhIQaxuCQ_lQzcPyQCP2wdcBAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAANGaqAs289CLn3G4iXwlQ2qTc19NqMAAhMQaxuCQ_lQZrVYSmUo-FgBAAMCAAN5AAM9BA",
        "correct_answer": "فلسطين",
    },
    {
        "id": 3,
        "spoiler_file_id": "AgACAgQAAxkBAANIaqAs_1Mgo_Rk_k61XAel0Cjv4_UAAhcQaxuCQ_lQrnaeVCCmlqUBAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAANKaqAtGyWLFr9jZlXAfm0jYwABjVXiAAIYEGsbgkP5UMue9vuE3KwfAQADAgADeQADPQQ",
        "correct_answer": "نهر",
    },
    {
        "id": 4,
        "spoiler_file_id": "AgACAgQAAxkBAANMaqAtTxxuoIuRhXG9rg8PjmyN0gYAAhsQaxuCQ_lQonX-GiGvR0ABAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAANOaqAtZEZ1yYrc3urKbC6OE2bZn5MAAhwQaxuCQ_lQ5RpqogXTdcwBAAMCAAN5AAM9BA",
        "correct_answer": "حصان",
    },
    {
        "id": 5,
        "spoiler_file_id": "AgACAgQAAxkBAANQaqAtin0MA5uPFhoTF856_tu94VoAAhQQaxuCQ_lQurm7lNhplX8BAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAANSaqAtoDkx1O6dJqiHDwqUmDVK_XAAAhUQaxuCQ_lQXf340sWTw1kBAAMCAAN5AAM9BA",
        "correct_answer": "غزة",
    },
    {
        "id": 6,
        "spoiler_file_id": "AgACAgQAAxkBAANUaqAtwvkLleeGd7OF4lc46UHGUzoAAhAQaxuCQ_lQsctSybnGxCIBAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAANVaqAtws89aT4jAZRE35mTc3DO-kQAAgIQaxssGwFRJYNfO7hPSWcBAAMCAAN5AAM9BA",
        "correct_answer": "بغداد",
    },
    {
        "id": 7,
        "spoiler_file_id": "AgACAgQAAxkBAANaaqAt_jdwXhrEQxIEiHP9l_j1qZgAAh8QaxuCQ_lQ9QXmLInTwM0BAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAANcaqAuGLaD0kSi8QVMAAGID4moK1CWAAIgEGsbgkP5UDqEWU__jjYrAQADAgADeQADPQQ",
        "correct_answer": "الرياض",
    },
    {
        "id": 8,
        "spoiler_file_id": "AgACAgQAAxkBAANeaqAuNtbhwZRvGCPoVU1zdQ-UvPgAAiMQaxuCQ_lQ-hyLMVj2Br0BAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAANgaqAuR4m2k5AaBQ-yyArF48MUppkAAiQQaxuCQ_lQvTUhaEbqYWwBAAMCAAN5AAM9BA",
        "correct_answer": "دمشق",
    },
    {
        "id": 9,
        "spoiler_file_id": "AgACAgQAAxkBAANiaqAuY8121rcioTe6e0KgfNlf7-wAAiIQaxuCQ_lQ0UNwZgABltyqAQADAgADeQADPQQ",
        "answer_file_id": "AgACAgQAAxkBAANkaqAuekfIbf9BWYm_jECHk6I-GzAAAiEQaxuCQ_lQbXCi8E_JRLkBAAMCAAN5AAM9BA",
        "correct_answer": "الاردن",
    },
    {
        "id": 10,
        "spoiler_file_id": "AgACAgQAAxkBAANmaqAuktj2tTLrL5eSd1Dvhhf4f7MAAiUQaxuCQ_lQiZV2J7CYgtYBAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAANoaqAuo0PV0QNGDLgtamwFULqGmbgAAiYQaxuCQ_lQ77b3xsobaSoBAAMCAAN5AAM9BA",
        "correct_answer": "لبنان",
    },
    {
        "id": 11,
        "spoiler_file_id": "AgACAgQAAyEFAAMBBkOLQwACBC5qn85CxQod0DBNiYnt-pnNneHX_AACJxBrG4JD-VCHvVjJbRuIaAEAAwIAA3kAAz0E",
        "answer_file_id": "AgACAgQAAxkBAANsaqAu15elw03cHTT9tebeluCsqiUAAigQaxuCQ_lQAAEf-rVVxsDeAQADAgADeQADPQQ",
        "correct_answer": "أسد",
    },
    {
        "id": 12,
        "spoiler_file_id": "AgACAgQAAxkBAANuaqAu8-isjRw_Uz4nMKyjE_6QJZEAAikQaxuCQ_lQJEQTFxljN1cBAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAANwaqAvBYbeCUUretGYIwLJRXyPE5IAAioQaxuCQ_lQMnM17xfQqkUBAAMCAAN5AAM9BA",
        "correct_answer": "وتين",
    },
    {
        "id": 13,
        "spoiler_file_id": "AgACAgQAAxkBAANyaqAvH_wMc7oNmNrCHaB_dW-jj10AAisQaxuCQ_lQSnQVZISiLgoBAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAAM2aqANnMCTXKWuwWc0p6qpmFnJwA0AAiwQaxuCQ_lQ_qsoNnkzdjMBAAMCAAN5AAM9BA",
        "correct_answer": "لؤي",
    },
    {
        "id": 14,
        "spoiler_file_id": "AgACAgQAAxkBAAN2aqAvTBzGwNj9cvyQHrA45gzvIAYAAgsQaxuCQ_lQ8FN_hbKiskwBAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAAN4aqAvYjDMcwABOBKLKUPHssQd1cQvAAIKEGsbgkP5UBcxiYnW902wAQADAgADeQADPQQ",
        "correct_answer": "فرح",
    },
    {
        "id": 15,
        "spoiler_file_id": "AgACAgQAAxkBAAN6aqAvjxz1aK-r0XgxkGFy6LlFC98AAgcQaxuCQ_lQtCkYqZYRYAkBAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAAN8aqAvrBlNC01hQsZSBFldMJCHHhoAAgkQaxuCQ_lQUjdam1WVWIYBAAMCAAN5AAM9BA",
        "correct_answer": "فاتن",
    },
    {
        "id": 16,
        "spoiler_file_id": "AgACAgQAAxkBAAN-aqAvyiF20DHcBIDhOOWOJUlXxHoAAi0QaxuCQ_lQUeSFSaJZ-igBAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAAOAaqAv4ENSx3doUnRqHLuJICtF5-4AAi4QaxuCQ_lQfWuQhWcGAn4BAAMCAAN5AAM9BA",
        "correct_answer": "هلا",
    },
    {
        "id": 17,
        "spoiler_file_id": "AgACAgQAAxkBAAOCaqAv_0MZtJm3dkSQ1Ke9mjTweOQAAg8QaxuCQ_lQQt_P1T-R9XQBAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAAOEaqAwEnLm_BYyGfQexn2okJU2mEEAAgUQaxssGwFR93WX14yDDCABAAMCAAN5AAM9BA",
        "correct_answer": "دانيا",
    },
    {
        "id": 18,
        "spoiler_file_id": "AgACAgQAAxkBAAOGaqAwL50YBnWF8eJRg_yQ-0Exf2cAAhkQaxuCQ_lQuvd3nrNyVH0BAAMCAAN5AAM9BA",
        "answer_file_id": "AgACAgQAAxkBAAOIaqAwQ7rIF1JSB7WYnWWedqYLawcAAhoQaxuCQ_lQT4tmcQAB4VBYAQADAgADeQADPQQ",
        "correct_answer": "انس",
    },
]

WIN_TARGET = 5
ENCOURAGEMENT_INTERVAL = 10

active_games = {}
user_scores = {}
game_locks = {}

def get_game_lock(chat_id):
    if chat_id not in game_locks:
        game_locks[chat_id] = asyncio.Lock()
    return game_locks[chat_id]

def normalize_answer(text):
    if not text:
        return ""
    text = str(text).strip().lower()
    text = "".join(
        char for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )
    replacements = {"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ي", "ة": "ه"}
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace("ـ", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def get_current_game(chat_id):
    game = active_games.get(chat_id)
    if not game:
        return None
    question_index = game.get("question_index", 0)
    if question_index >= len(GAMES_LIST):
        question_index = 0
        game["question_index"] = 0
    return GAMES_LIST[question_index]

def create_score_button():
    keyboard = [[InlineKeyboardButton("📊 دفتر النتائج", callback_data="show_scoreboard")]]
    return InlineKeyboardMarkup(keyboard)

def create_scoreboard_keyboard():
    keyboard = [[InlineKeyboardButton("❌ إغلاق", callback_data="close_score")]]
    return InlineKeyboardMarkup(keyboard)

def build_scoreboard_text(chat_id):
    scores = user_scores.get(chat_id, {})
    if not scores:
        return (
            "📊 <b>╔════════════════════╗</b>\n"
            "🏆 <b>دَفـتـر نـتـائـج الـغـبـاش</b> 🏆\n"
            "📊 <b>╚════════════════════╝</b>\n\n"
            "📭 <b>لا توجد نقاط مسجلة حتى الآن.</b>"
        )
    sorted_users = sorted(
        scores.values(),
        key=lambda item: (item.get("points", 0), item.get("name", "")),
        reverse=True
    )
    score_text = (
        "📊 <b>╔════════════════════════╗</b>\n"
        "🏆 <b>   دَفـتـر نـتـائـج الـغـبـاش   </b> 🏆\n"
        "📊 <b>╚════════════════════════╝</b>\n\n"
    )
    limit = min(len(sorted_users), 10)
    for index in range(limit):
        item = sorted_users[index]
        name = html.escape(item.get("name", "المتحدي"))
        points = item.get("points", 0)
        score_text += f"🏅 <b>{index + 1}. {name}</b>\n   ⭐ <b>{points} نقطة</b>\n"
        if index < limit - 1:
            score_text += "━━━━━━━━━━━━━━━━━━━━\n"
    return score_text

async def encouragement_loop(application, chat_id):
    try:
        while True:
            await asyncio.sleep(ENCOURAGEMENT_INTERVAL)
            game = active_games.get(chat_id)
            if not game or game.get("winner_found", False):
                break
            encouraging_text = (
                "⏳ <b>━━━━━━━━━━━━━━━━━━</b> ⏳\n"
                "🔥 <b>تـحـدي الـغـبـاش مـسـتـمـر!</b> 🔥\n"
                "💎 <b>مـا زال الـلـغـز بـانـتـظـار الـحـل!</b> 💎\n"
                "⏳ <b>━━━━━━━━━━━━━━━━━━</b> ⏳\n\n"
                "⚡ <b>أيـن أنـتـم يـا عـشـاق الـتـحـدي؟!</b> ⚡\n\n"
                "🧩 <b>اكـشـفـوا الـصـورة...</b>\n"
                "🧠 <b>واجـمـعـوا الأحـرف...</b>\n"
                "🏆 <b>وأثـبـتـوا أنـكـم أسـاطـيـر الـغـبـاش!</b> 🏆"
            )
            try:
                await application.bot.send_message(chat_id=chat_id, text=encouraging_text, parse_mode="HTML")
            except Exception as e:
                print(f"❌ خطأ في رسالة التشجيع للمجموعة {chat_id}: {e}")
                break
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"❌ خطأ غير متوقع في encouragement_loop للمجموعة {chat_id}: {e}")

def cancel_encouragement_task(chat_id):
    game = active_games.get(chat_id)
    if not game:
        return
    task = game.get("encouragement_task")
    if task and not task.done():
        task.cancel()
    game["encouragement_task"] = None

async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text or not update.effective_chat:
        return
    chat = update.effective_chat
    chat_id = chat.id

    if chat.type not in ["group", "supergroup"]:
        return

    if not GAMES_LIST:
        await update.message.reply_text("❌ عذراً، لا توجد أسئلة مخزنة حالياً.")
        return

    lock = get_game_lock(chat_id)
    async with lock:
        if chat_id in active_games:
            game = active_games[chat_id]
            if not game.get("winner_found", False):
                await update.message.reply_text(
                    "⏳ <b>السؤال الحالي ما زال مفتوحاً!</b>\n\n"
                    "🏆 <b>أجيبوا على السؤال أولاً، وبعد ظهور الإجابة الصحيحة يمكن كتابة «غباش» لبدء السؤال التالي.</b>",
                    parse_mode="HTML"
                )
                return

        if chat_id not in active_games:
            active_games[chat_id] = {"question_index": 0, "winner_found": False, "encouragement_task": None}
        else:
            game = active_games[chat_id]
            game["winner_found"] = False

        cancel_encouragement_task(chat_id)
        q_data = get_current_game(chat_id)
        if not q_data:
            await update.message.reply_text("❌ حدث خطأ في تحميل سؤال اللعبة.")
            return

        start_msg_text = (
            "👑 <b>╔══════════════════════╗</b>\n"
            "👑 <b>   تـحـدي الـغـبـاش الـمـلـكـي   </b> 👑\n"
            "👑 <b>╚══════════════════════╝</b>\n\n"
            "🔥 <b>يـا أسـاطـيـر شـعـب مـونـوبـولـي الـعـظـيـم</b> 🔥\n\n"
            "🎯 <b>لـقـد بـدأ الـتـحـدي!</b> 🎯\n\n"
            "🧩 <b>طـريـقـة الـلـعـب:</b>\n"
            "👆 <b>اضـغـطـوا عـلـى صـورة الـغـبـاش لـكـشـفـهـا</b>\n"
            "🔤 <b>اجـمـعـوا الأحـرف الـظـاهـرة فـي الـصـورة</b>\n"
            "🧠 <b>اكـتـبـوا الـكـلـمـة الـصـحـيـحـة فـي الـمـجـمـوعـة</b>\n\n"
            "🏆 <b>الـفـوز لـمـن يـكـتـشـف الـكـلـمـة أولاً!</b> 🏆\n"
            "⚡ <b>حـظـاً مـوفـقـاً لـجـمـيـع الـمـتـحـديـن!</b> ⚡"
        )

        try:
            await context.bot.send_message(chat_id=chat_id, text=start_msg_text, parse_mode="HTML")
        except Exception as e:
            print(f"❌ خطأ في إرسال رسالة بداية الغباش للمجموعة {chat_id}: {e}")
            return

        # إرسال الصورة بدون أزرار عند البدء
        try:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=q_data["spoiler_file_id"],
                has_spoiler=True,
            )
            print(f"✅ تم إرسال صورة الغباش للمجموعة {chat_id} السؤال {q_data['id']}")
        except Exception as e:
            print(f"❌ خطأ في إرسال صورة الغباش للمجموعة {chat_id}: {e}")
            await update.message.reply_text("❌ حدث خطأ أثناء إرسال صورة الغباش.")
            return

        task = asyncio.create_task(encouragement_loop(context.application, chat_id))
        active_games[chat_id]["encouragement_task"] = task


# =========================================================
# معالجة تفاعلات الأزرار (دفتر النتائج) - بدون تقييد بالـ Pattern
# =========================================================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or not query.data or not query.message:
        return

    chat_id = query.message.chat_id
    data = query.data

    print(f"📥 تم استقبال ضغطة زر بقيمة: {data} من المجموعة: {chat_id}")

    if data == "show_scoreboard":
        scoreboard_text = build_scoreboard_text(chat_id)
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=scoreboard_text,
                parse_mode="HTML",
                reply_markup=create_scoreboard_keyboard(),
            )
        except Exception as e:
            print(f"❌ خطأ في إرسال دفتر النتائج: {e}")

        try:
            await query.answer("📊 إليك دفتر النتائج")
        except Exception:
            pass
        return

    if data == "close_score":
        try:
            await query.message.delete()
        except Exception as e:
            print(f"⚠️ تعذر حذف دفتر النتائج: {e}")
        try:
            await query.answer("تم الإغلاق")
        except Exception:
            pass
        return

    try:
        await query.answer()
    except Exception:
        pass


# =========================================================
# تسجيل الـ Handlers (في نهاية ملف bot.py)
# =========================================================

def setup_game_handlers(app):
    app.add_handler(CommandHandler("غباش", start_game))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_game_message))
    app.add_handler(CallbackQueryHandler(callback_handler))
