# bot.py

import asyncio
import html

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



# =========================================================
# حالة الألعاب
# =========================================================

# لكل مجموعة:
#
# active_games[chat_id] = {
#     "question_index": 0,
#     "winner_found": False,
#     "encouragement_task": task
# }
#
active_games = {}


# النقاط:
#
# user_scores[chat_id][user_id] = {
#     "name": "...",
#     "score": 0
# }
#
user_scores = {}


# =========================================================
# أدوات مساعدة
# =========================================================

def get_current_game(chat_id):
    """
    الحصول على بيانات السؤال الحالي للمجموعة.
    """
    game = active_games.get(chat_id)

    if not game:
        return None

    question_index = game.get("question_index", 0)

    if question_index >= len(GAMES_LIST):
        question_index = 0
        game["question_index"] = 0

    return GAMES_LIST[question_index]


def create_score_button():
    """
    زر دفتر النتائج.
    """
    keyboard = [
        [
            InlineKeyboardButton(
                "📊 دفتر النتائج",
                callback_data="show_scoreboard"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def create_scoreboard_keyboard():
    """
    أزرار دفتر النتائج.
    """
    keyboard = [
        [
            InlineKeyboardButton(
                "◀️ السابق",
                callback_data="prev_score"
            ),
            InlineKeyboardButton(
                "التالي ▶️",
                callback_data="next_score"
            ),
        ],
        [
            InlineKeyboardButton(
                "❌ إغلاق",
                callback_data="close_score"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# رسالة التشجيع
# =========================================================

async def encouragement_loop(application, chat_id):
    try:
        while True:
            await asyncio.sleep(10)

            if chat_id not in active_games:
                break

            if active_games[chat_id].get("winner_found", False):
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
                await application.bot.send_message(
                    chat_id=chat_id,
                    text=encouraging_text,
                    parse_mode="HTML"
                )

            except Exception as e:
                print(
                    f"❌ خطأ في رسالة التشجيع "
                    f"للمجموعة {chat_id}: {e}"
                )
                break

    except asyncio.CancelledError:
        pass

    except Exception as e:
        print(
            f"❌ خطأ غير متوقع في encouragement_loop "
            f"للمجموعة {chat_id}: {e}"
        )




# =========================================================
# بدء لعبة الغباش
# =========================================================

async def start_game(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    if not update.message.text:
        return

    if not update.effective_chat:
        return

    chat_id = update.effective_chat.id

    # اللعبة تعمل فقط في المجموعات
    if update.effective_chat.type not in [
        "group",
        "supergroup"
    ]:
        return

    # لا توجد أسئلة
    if not GAMES_LIST:

        await update.message.reply_text(
            "❌ عذراً، لا توجد أسئلة مخزنة حالياً."
        )

        return

    # -----------------------------------------------------
    # إنشاء حالة اللعبة
    # -----------------------------------------------------

    if chat_id not in active_games:

        active_games[chat_id] = {
            "question_index": 0,
            "winner_found": False,
            "encouragement_task": None,
        }

    else:

        current_index = active_games[chat_id].get(
            "question_index",
            0
        )

        if current_index >= len(GAMES_LIST):

            active_games[chat_id]["question_index"] = 0

    # -----------------------------------------------------
    # إيقاف مهمة التشجيع القديمة إن وجدت
    # -----------------------------------------------------

    old_task = active_games[chat_id].get(
        "encouragement_task"
    )

    if old_task and not old_task.done():

        old_task.cancel()

    # -----------------------------------------------------
    # إعداد السؤال
    # -----------------------------------------------------

    active_games[chat_id]["winner_found"] = False

    q_data = get_current_game(chat_id)

    if not q_data:

        await update.message.reply_text(
            "❌ حدث خطأ في تحميل سؤال اللعبة."
        )

        return

    # -----------------------------------------------------
    # رسالة البداية
    # -----------------------------------------------------

    start_msg_text = (
    "👑 <b>╔══════════════════════╗</b>\n"
    "👑 <b>   تـحـدي الـغـبـاش الـمـلـكـي   </b> 👑\n"
    "👑 <b>╚══════════════════════╝</b>\n\n"
    
    "🔥 <b>يـا أسـاطـيـر شـعـب مـونـوبـولـي الـعـظـيـم</b> 🔥\n\n"
    
    "🎯 <b>لـقـد بـدأ الـتـحـدي!</b> 🎯\n\n"
    
    "🧩 <b>طريقة اللعب:</b>\n"
    "👆 <b>اضـغـطـوا عـلـى صـورة الـغـبـاش لـكـشـفـهـا</b>\n"
    "🔤 <b>اجـمـعـوا الأحـرف الـظـاهـرة فـي الـصـورة</b>\n"
    "🧠 <b>اكتـبـوا الـكـلـمـة الـصـحـيـحـة فـي الـمـجـمـوعـة</b>\n\n"
    
    "🏆 <b>الـفـوز لـمـن يـكـتـشـف الـكـلـمـة أولاً!</b> 🏆\n"
    "⚡ <b>حـظـاً مـوفـقـاً لـجـمـيـع الـمـتـحـديـن!</b> ⚡"
)


    try:

        await context.bot.send_message(
            chat_id=chat_id,
            text=start_msg_text,
            parse_mode="HTML",
        )

    except Exception as e:

        print(
            f"❌ خطأ في إرسال رسالة بداية الغباش: {e}"
        )

        return

    # -----------------------------------------------------
    # زر النتائج
    # -----------------------------------------------------

    reply_markup = create_score_button()

    # -----------------------------------------------------
    # إرسال صورة الغباش
    # -----------------------------------------------------

    try:

        await context.bot.send_photo(
            chat_id=chat_id,

            # مهم:
            # نستخدم file_id مباشرة بدون str()
            photo=q_data["spoiler_file_id"],

            reply_markup=reply_markup,

            # صورة مخفية Spoiler
            has_spoiler=True,
        )

        print(
            f"✅ تم إرسال صورة الغباش بنجاح "
            f"للمجموعة {chat_id}"
        )

    except Exception as e:

        import traceback

        print(
            "\n"
            "==========================================\n"
            "❌ خطأ في إرسال صورة الغباش\n"
            "=========================================="
        )

        print(
            "Chat ID:",
            chat_id
        )

        print(
            "Question ID:",
            q_data.get("id")
        )

        print(
            "File ID:",
            repr(q_data.get("spoiler_file_id"))
        )

        print(
            "Error Type:",
            type(e).__name__
        )

        print(
            "Error:",
            repr(e)
        )

        traceback.print_exc()

        print(
            "==========================================\n"
        )

        await update.message.reply_text(
            "❌ حدث خطأ أثناء إرسال صورة الغباش.\n"
            "راجع سجل السيرفر لمعرفة تفاصيل الخطأ."
        )

        return

    # -----------------------------------------------------
    # تشغيل التشجيع
    # -----------------------------------------------------

    task = asyncio.create_task(
        encouragement_loop(
            context.application,
            chat_id
        )
    )

    active_games[chat_id]["encouragement_task"] = task


# =========================================================
# استقبال إجابات اللاعبين
# =========================================================

async def handle_game_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    if not update.message.text:
        return

    if not update.effective_chat:
        return

    # اللعبة للمجموعات فقط
    if update.effective_chat.type not in [
        "group",
        "supergroup"
    ]:
        return

    chat_id = update.effective_chat.id

    # لا توجد لعبة نشطة
    if chat_id not in active_games:
        return

    # تم العثور على الفائز
    if active_games[chat_id].get(
        "winner_found",
        False
    ):
        return

    q_data = get_current_game(chat_id)

    if not q_data:
        return

    # -----------------------------------------------------
    # النص الذي كتبه اللاعب
    # -----------------------------------------------------

    user_text = update.message.text.strip()

    # تجاهل كلمة غباش نفسها
    if user_text == "غباش":
        return

    # -----------------------------------------------------
    # مقارنة الإجابة
    # -----------------------------------------------------

    correct_answer = q_data["correct_answer"].strip()

    if user_text != correct_answer:
        return

    # -----------------------------------------------------
    # تسجيل الفوز
    # -----------------------------------------------------

    active_games[chat_id]["winner_found"] = True

    # إيقاف التشجيع
    task = active_games[chat_id].get(
        "encouragement_task"
    )

    if task and not task.done():
        task.cancel()

    # -----------------------------------------------------
    # بيانات اللاعب
    # -----------------------------------------------------

    user = update.effective_user

    if not user:
        return

    user_id = user.id

    user_name = (
        user.first_name
        or "المتحدي"
    )

    # حماية اسم اللاعب عند استخدام HTML
    safe_user_name = html.escape(
        user_name
    )

    # -----------------------------------------------------
    # إنشاء سجل المجموعة
    # -----------------------------------------------------

    if chat_id not in user_scores:
        user_scores[chat_id] = {}

    # -----------------------------------------------------
    # إنشاء سجل اللاعب
    # -----------------------------------------------------

    if user_id not in user_scores[chat_id]:

        user_scores[chat_id][user_id] = {
            "name": user_name,
            "score": 0,
        }

    # تحديث الاسم في حال تغير
    else:

        user_scores[chat_id][user_id][
            "name"
        ] = user_name

    # -----------------------------------------------------
    # إضافة نقطة
    # -----------------------------------------------------

    user_scores[chat_id][user_id]["score"] += 1

    current_score = user_scores[
        chat_id
    ][user_id]["score"]

    # -----------------------------------------------------
    # زر دفتر النتائج
    # -----------------------------------------------------

    reply_markup = create_score_button()

    # -----------------------------------------------------
    # إرسال الصورة الصحيحة
    # -----------------------------------------------------

    try:

        await update.message.reply_photo(

    # نستخدم file_id مباشرة
    photo=q_data["answer_file_id"],

    caption=(
    "🏆 <b>╔════════════════════╗</b> 🏆\n"
    "✨ <b>مـبـرووووك يـا بـطـل!</b> ✨\n"
    "🏆 <b>╚════════════════════╝</b> 🏆\n\n"

    "🎉 <b>إجـابـتـك صـحـيـحـة ١٠٠٪</b> 🎉\n\n"

    "💎 <b>أبـدعـت فـي تـحـدي الـغـبـاش!</b> 💎\n"
    "🔥 <b>نـقـطـة جـديـدة تُـضـاف إلـى رصـيـدك</b> 🔥\n\n"

    "👑 <b>اسـتـمـر فـي الـتـحـدي... والـقـادم أصـعـب!</b> 👑"
),


            parse_mode="HTML",

            reply_markup=reply_markup,
        )

        print(
            f"✅ تم إرسال الصورة الصحيحة "
            f"للاعب {user_id}"
        )

    except Exception as e:

        import traceback

        print(
            "\n"
            "==========================================\n"
            "❌ خطأ في إرسال صورة الإجابة\n"
            "=========================================="
        )

        print(
            "Chat ID:",
            chat_id
        )

        print(
            "User ID:",
            user_id
        )

        print(
            "Answer File ID:",
            repr(q_data.get("answer_file_id"))
        )

        print(
            "Error Type:",
            type(e).__name__
        )

        print(
            "Error:",
            repr(e)
        )

        traceback.print_exc()

        print(
            "==========================================\n"
        )

        # حتى لو فشل إرسال الصورة،
        # لا نعيد الجولة لنفس الإجابة
        await update.message.reply_text(
            "✅ إجابتك صحيحة، لكن حدث خطأ "
            "أثناء إرسال الصورة الصحيحة."
        )

    # -----------------------------------------------------
    # الوصول إلى 5 انتصارات
    # -----------------------------------------------------

    if current_score >= 5:

        congrats_msg = (
    "🏆 <b>━━━━━━━━━━━━━━━━━━━━</b> 🏆\n"
    "👑 <b>تـهـانـيـنـا لـأسـطـورة الـغـبـاش</b> 👑\n"
    "🏆 <b>━━━━━━━━━━━━━━━━━━━━</b> 🏆\n\n"

    f"✨ <b><a href='tg://user?id={user_id}'>"
    f"{safe_user_name}"
    "</a></b> ✨\n\n"

    "🔥 <b>خـمـسـة انـتـصـارات مـتـتـالـيـة!</b> 🔥\n"
    "💎 <b>لـقـد أثـبـتَّ أنـك مـن أسـاطـيـر الـغـبـاش</b> 💎\n\n"

    "🥇 <b>الـمـركـز الـذهـبـي يـلـيـق بـك!</b> 🥇\n"
    "⚡ <b>هـل تـسـتـطـيـع الـعـودة وإثـبـات نـفـسـك مـن جـديـد؟</b> ⚡"
)


        try:

            await context.bot.send_message(
                chat_id=chat_id,
                text=congrats_msg,
                parse_mode="HTML",
            )

        except Exception as e:

            print(
                f"❌ خطأ في إرسال رسالة الخمس انتصارات: {e}"
            )

        # تصفير النقاط بعد الوصول إلى 5
        user_scores[chat_id][user_id]["score"] = 0

    # -----------------------------------------------------
    # الانتقال للسؤال التالي
    # -----------------------------------------------------

    active_games[chat_id]["question_index"] += 1

    # إذا وصلنا لنهاية الأسئلة
    if active_games[chat_id]["question_index"] >= len(
        GAMES_LIST
    ):

        active_games[chat_id]["question_index"] = 0


# =========================================================
# دفتر النتائج
# =========================================================

async def show_scoreboard(
    query,
    context
):

    if not query.message:
        await query.answer()
        return

    chat_id = query.message.chat_id

    # لا يوجد لاعبين
    if (
        chat_id not in user_scores
        or not user_scores[chat_id]
    ):

        await query.answer(
            "دفتر النتائج فارغ حتى الآن، كن أول الفائزين!",
            show_alert=True,
        )

        return

    # ترتيب اللاعبين
    sorted_users = sorted(
        user_scores[chat_id].values(),
        key=lambda x: x["score"],
        reverse=True,
    )

    # -----------------------------------------------------
    # إنشاء التقرير
    # -----------------------------------------------------

    score_text = (
        "📊 <b>--- دفتر النتائج والمراتب ---</b> 📊\n\n"
    )

    for idx, item in enumerate(
        sorted_users[:10],
        start=1
    ):

        safe_name = html.escape(
            str(item["name"])
        )

        score_text += (
            f"🏅 <b>{idx}. {safe_name}</b>"
            f" ⟵ <b>{item['score']}</b> انتصارات\n"
        )

    # -----------------------------------------------------
    # إرسال دفتر النتائج
    # -----------------------------------------------------

    try:

        await query.message.reply_text(
            text=score_text,
            parse_mode="HTML",
            reply_markup=create_scoreboard_keyboard(),
        )

        await query.answer()

    except Exception as e:

        print(
            f"❌ خطأ في عرض دفتر النتائج: {e}"
        )

        try:
            await query.answer(
                "حدث خطأ أثناء عرض دفتر النتائج.",
                show_alert=True,
            )
        except Exception:
            pass


# =========================================================
# Callback Query
# =========================================================

async def callback_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if not query:
        return

    if not query.data:
        return

    data = query.data

    # -----------------------------------------------------
    # دفتر النتائج
    # -----------------------------------------------------

    if data == "show_scoreboard":

        await show_scoreboard(
            query,
            context
        )

        return

    # -----------------------------------------------------
    # إغلاق النتائج
    # -----------------------------------------------------

    if data == "close_score":

        try:

            if query.message:
                await query.message.delete()

        except Exception as e:

            print(
                f"⚠️ تعذر حذف دفتر النتائج: {e}"
            )

        try:
            await query.answer()
        except Exception:
            pass

        return

    # -----------------------------------------------------
    # الصفحات
    # -----------------------------------------------------

    if data in [
        "prev_score",
        "next_score"
    ]:

        await query.answer(
            "حالياً جميع النتائج موجودة في الصفحة الحالية.",
            show_alert=True,
        )

        return


# =========================================================
# تسجيل Handlers
# =========================================================

def setup_game_handlers(app):

    """
    تسجيل جميع Handlers الخاصة بلعبة الغباش.

    مهم:
    هذه الدالة مصممة للعمل مع
    python-telegram-bot Application
    الموجود في main.py
    """

    # -----------------------------------------------------
    # بدء لعبة الغباش
    # -----------------------------------------------------

    app.add_handler(
        MessageHandler(
            filters.Regex(r"^غباش$"),
            start_game,
        ),
        group=10,
    )

    # -----------------------------------------------------
    # استقبال إجابات اللاعبين
    #
    # group=11 حتى يأتي بعد start_game
    # -----------------------------------------------------

    app.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND,
            handle_game_message,
        ),
        group=11,
    )

    # -----------------------------------------------------
    # أزرار دفتر النتائج
    # -----------------------------------------------------

    app.add_handler(
        CallbackQueryHandler(
            callback_handler,
            pattern=r"^(show_scoreboard|close_score|prev_score|next_score)$",
        ),
        group=10,
    )

    print(
        "✅ تم تحميل نظام لعبة الغباش بنجاح."
    )
