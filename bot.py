# bot.py

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


# =========================================================
# إعدادات اللعبة
# =========================================================

WIN_TARGET = 5
ENCOURAGEMENT_INTERVAL = 10


# =========================================================
# حالة الألعاب
# =========================================================

# active_games[chat_id] = {
#     "question_index": 0,
#     "winner_found": False,
#     "encouragement_task": task
# }

active_games = {}


# =========================================================
# النتائج
# =========================================================

# user_scores[chat_id][user_id] = {
#     "name": "...",
#     "points": 0,   # النقاط التراكمية
#     "streak": 0    # عداد الفوز المتتالي من 5
# }

user_scores = {}


# =========================================================
# أقفال المجموعات
# =========================================================

# يمنع تسجيل فائزين في نفس الجولة
# إذا وصلت إجابتان في نفس اللحظة تقريبًا.

game_locks = {}


def get_game_lock(chat_id):
    if chat_id not in game_locks:
        game_locks[chat_id] = asyncio.Lock()

    return game_locks[chat_id]


# =========================================================
# تنظيف الإجابات
# =========================================================

def normalize_answer(text):
    """
    توحيد الإجابة العربية قبل المقارنة.

    مثال:
    الأردن
    الاردن

    سيتم اعتبارهما نفس الإجابة.
    """

    if not text:
        return ""

    text = text.strip().lower()

    # إزالة التشكيل
    text = "".join(
        char
        for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )

    # توحيد بعض الحروف العربية
    replacements = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ٱ": "ا",
        "ى": "ي",
        "ة": "ه",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # إزالة التطويل
    text = text.replace("ـ", "")

    # إزالة المسافات الزائدة
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# الحصول على السؤال الحالي
# =========================================================

def get_current_game(chat_id):

    game = active_games.get(chat_id)

    if not game:
        return None

    question_index = game.get(
        "question_index",
        0
    )

    if question_index >= len(GAMES_LIST):

        question_index = 0

        game["question_index"] = 0

    return GAMES_LIST[question_index]


# =========================================================
# زر دفتر النتائج
# =========================================================

def create_score_button():

    keyboard = [
        [
            InlineKeyboardButton(
                "📊 دفتر النتائج",
                callback_data="show_scoreboard"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# أزرار دفتر النتائج
# =========================================================

def create_scoreboard_keyboard():

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
# بناء دفتر النتائج
# =========================================================

def build_scoreboard_text(chat_id):

    scores = user_scores.get(chat_id, {})

    if not scores:
        return (
            "📊 <b>╔════════════════════╗</b>\n"
            "🏆 <b>دَفـتـر نـتـائـج الـغـبـاش</b> 🏆\n"
            "📊 <b>╚════════════════════╝</b>\n\n"
            "📭 <b>لا توجد نقاط مسجلة حتى الآن.</b>"
        )

    # الترتيب حسب النقاط التراكمية
    sorted_users = sorted(
        scores.values(),
        key=lambda item: item.get("points", 0),
        reverse=True
    )

    score_text = (
        "📊 <b>╔════════════════════════╗</b>\n"
        "🏆 <b>   دَفـتـر نـتـائـج الـغـبـاش   </b> 🏆\n"
        "📊 <b>╚════════════════════════╝</b>\n\n"
    )

    for index, item in enumerate(
        sorted_users[:10],
        start=1
    ):

        name = html.escape(
            item.get("name", "المتحدي")
        )

        points = item.get(
            "points",
            0
        )

        score_text += (
            f"🏅 <b>{index}. {name}</b>\n"
            f"   ⭐ <b>{points} نقطة</b>\n"
        )

        # فاصل عريض بين اللاعبين
        if index < min(
            len(sorted_users),
            10
        ):
            score_text += (
                "━━━━━━━━━━━━━━━━━━━━\n"
            )

    return score_text


# =========================================================
# رسالة التشجيع
# =========================================================

async def encouragement_loop(
    application,
    chat_id
):

    try:

        while True:

            await asyncio.sleep(
                ENCOURAGEMENT_INTERVAL
            )

            if chat_id not in active_games:
                break

            if active_games[chat_id].get(
                "winner_found",
                False
            ):
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
            f"❌ خطأ غير متوقع في "
            f"encouragement_loop "
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

    chat = update.effective_chat

    chat_id = chat.id

    # اللعبة تعمل في المجموعات فقط
    if chat.type not in [
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

        current_index = active_games[
            chat_id
        ].get(
            "question_index",
            0
        )

        if current_index >= len(
            GAMES_LIST
        ):

            active_games[
                chat_id
            ]["question_index"] = 0

    # -----------------------------------------------------
    # إلغاء التشجيع القديم
    # -----------------------------------------------------

    old_task = active_games[
        chat_id
    ].get(
        "encouragement_task"
    )

    if old_task and not old_task.done():

        old_task.cancel()

    # -----------------------------------------------------
    # تجهيز الجولة
    # -----------------------------------------------------

    active_games[
        chat_id
    ]["winner_found"] = False

    q_data = get_current_game(
        chat_id
    )

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

        "🧩 <b>طـريـقـة الـلـعـب:</b>\n"
        "👆 <b>اضـغـطـوا عـلـى صـورة الـغـبـاش لـكـشـفـهـا</b>\n"
        "🔤 <b>اجـمـعـوا الأحـرف الـظـاهـرة فـي الـصـورة</b>\n"
        "🧠 <b>اكـتـبـوا الـكـلـمـة الـصـحـيـحـة فـي الـمـجـمـوعـة</b>\n\n"

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
            f"❌ خطأ في إرسال رسالة "
            f"بداية الغباش: {e}"
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
            photo=q_data[
                "spoiler_file_id"
            ],
            reply_markup=reply_markup,
            has_spoiler=True,
        )

        print(
            f"✅ تم إرسال صورة الغباش "
            f"للمجموعة {chat_id} "
            f"السؤال {q_data['id']}"
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
            repr(
                q_data.get(
                    "spoiler_file_id"
                )
            )
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
            "❌ حدث خطأ أثناء إرسال صورة الغباش."
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

    active_games[
        chat_id
    ]["encouragement_task"] = task


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

    chat = update.effective_chat

    # مجموعات فقط
    if chat.type not in [
        "group",
        "supergroup"
    ]:
        return

    chat_id = chat.id

    # لا توجد لعبة
    if chat_id not in active_games:
        return

    # -----------------------------------------------------
    # كلمة غباش تبدأ اللعبة من خلال start_game
    # لذلك لا نعالجها كإجابة
    # -----------------------------------------------------

    user_text = update.message.text.strip()

    if normalize_answer(
        user_text
    ) == normalize_answer("غباش"):

        return

    # -----------------------------------------------------
    # القفل مهم جدًا
    # لمنع فوز شخصين في نفس السؤال
    # -----------------------------------------------------

    lock = get_game_lock(
        chat_id
    )

    async with lock:

        # إعادة الفحص بعد الحصول على القفل
        if chat_id not in active_games:
            return

        game = active_games[
            chat_id
        ]

        if game.get(
            "winner_found",
            False
        ):
            return

        # -------------------------------------------------
        # السؤال الحالي
        # -------------------------------------------------

        q_data = get_current_game(
            chat_id
        )

        if not q_data:
            return

        # -------------------------------------------------
        # مقارنة الإجابة
        # -------------------------------------------------

        correct_answer = normalize_answer(
            q_data[
                "correct_answer"
            ]
        )

        submitted_answer = normalize_answer(
            user_text
        )

        if submitted_answer != correct_answer:
            return

        # -------------------------------------------------
        # تسجيل الفائز فورًا
        # -------------------------------------------------

        game[
            "winner_found"
        ] = True

        # -------------------------------------------------
        # إيقاف التشجيع
        # -------------------------------------------------

        task = game.get(
            "encouragement_task"
        )

        if task and not task.done():

            task.cancel()

        # -------------------------------------------------
        # بيانات اللاعب
        # -------------------------------------------------

        user = update.effective_user

        if not user:
            return

        user_id = user.id

        user_name = (
            user.first_name
            or "المتحدي"
        )

        safe_user_name = html.escape(
            user_name
        )

        # -------------------------------------------------
        # إنشاء سجل المجموعة
        # -------------------------------------------------

        if chat_id not in user_scores:

            user_scores[
                chat_id
            ] = {}

        # -------------------------------------------------
        # إنشاء سجل اللاعب
        # -------------------------------------------------

        if user_id not in user_scores[
            chat_id
        ]:

            user_scores[
                chat_id
            ][user_id] = {
                "name": user_name,
                "points": 0,
                "streak": 0,
            }

        else:

            user_scores[
                chat_id
            ][user_id][
                "name"
            ] = user_name

        player = user_scores[
            chat_id
        ][user_id]

        # -------------------------------------------------
        # إضافة نقطة تراكمية
        # -------------------------------------------------

        player[
            "points"
        ] += 1

        # -------------------------------------------------
        # إضافة فوز متتالي للاعب نفسه
        # -------------------------------------------------

        player[
            "streak"
        ] += 1

        current_streak = player[
            "streak"
        ]

        total_points = player[
            "points"
        ]

        # -------------------------------------------------
        # إرسال الصورة الصحيحة
        # -------------------------------------------------

        try:

            await update.message.reply_photo(

                photo=q_data[
                    "answer_file_id"
                ],

                caption=(
                    "🏆 <b>╔════════════════════╗</b> 🏆\n"
                    "✨ <b>مـبـرووووك يـا بـطـل!</b> ✨\n"
                    "🏆 <b>╚════════════════════╝</b> 🏆\n\n"

                    "🎉 <b>إجـابـتـك صـحـيـحـة ١٠٠٪</b> 🎉\n\n"

                    f"🥇 <b>الـفـوز رقـم "
                    f"{current_streak} / {WIN_TARGET}</b> 🥇\n\n"

                    f"⭐ <b>رصـيـدك الـتـراكـمـي: "
                    f"{total_points} نـقـطـة</b> ⭐\n\n"

                    "💎 <b>أبـدعـت فـي تـحـدي الـغـبـاش!</b> 💎\n"
                    "🔥 <b>نـقـطـة جـديـدة تُـضـاف إلـى رصـيـدك</b> 🔥\n\n"

                    "👑 <b>اسـتـمـر فـي الـتـحـدي... "
                    "والـقـادم أصـعـب!</b> 👑"
                ),

                parse_mode="HTML",

                reply_markup=create_score_button(),
            )

            print(
                f"✅ فوز صحيح | "
                f"المجموعة: {chat_id} | "
                f"المستخدم: {user_id} | "
                f"الاسم: {user_name} | "
                f"النقاط: {total_points} | "
                f"التتابع: {current_streak}/{WIN_TARGET}"
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
                "User Name:",
                user_name
            )

            print(
                "Question ID:",
                q_data.get("id")
            )

            print(
                "Answer File ID:",
                repr(
                    q_data.get(
                        "answer_file_id"
                    )
                )
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
                (
                    f"✅ <b>إجابتك صحيحة!</b>\n\n"
                    f"🥇 <b>الفوز رقم "
                    f"{current_streak} / {WIN_TARGET}</b>\n"
                    f"⭐ <b>رصيدك التراكمي: "
                    f"{total_points} نقطة</b>"
                ),
                parse_mode="HTML",
                reply_markup=create_score_button(),
            )

        # -------------------------------------------------
        # هل وصل اللاعب إلى 5 / 5؟
        # -------------------------------------------------

        reached_five = (
            current_streak >= WIN_TARGET
        )

        if reached_five:

            congrats_msg = (
                "🏆 <b>╔════════════════════════╗</b> 🏆\n"
                "👑 <b>تـهـانـيـنـا لـأسـطـورة الـغـبـاش!</b> 👑\n"
                "🏆 <b>╚════════════════════════╝</b> 🏆\n\n"

                f"✨ <b><a href='tg://user?id={user_id}'>"
                f"{safe_user_name}"
                f"</a></b> ✨\n\n"

                "🔥 <b>خـمـسـة انـتـصـارات مـتـتـالـيـة!</b> 🔥\n\n"

                "💎 <b>لـقـد أثـبـتَّ أنـك مـن "
                "أسـاطـيـر تـحـدي الـغـبـاش!</b> 💎\n\n"

                "🥇 <b>أنـت الآن بطل الجولة!</b> 🥇\n"
                "⚡ <b>والآن... هل تستطيع أن تبدأ من جديد؟</b> ⚡"
            )

            try:

                await context.bot.send_message(
                    chat_id=chat_id,
                    text=congrats_msg,
                    parse_mode="HTML",
                )

            except Exception as e:

                print(
                    f"❌ خطأ في إرسال رسالة "
                    f"الخمس انتصارات: {e}"
                )

            # -------------------------------------------------
            # تصفير عداد الفوز فقط
            #
            # النقاط التراكمية لا تتغير
            # -------------------------------------------------

            player[
                "streak"
            ] = 0

            # -------------------------------------------------
            # إرسال دفتر النتائج بعد رسالة الفوز
            # -------------------------------------------------

            scoreboard_text = build_scoreboard_text(
                chat_id
            )

            try:

                await context.bot.send_message(
                    chat_id=chat_id,
                    text=scoreboard_text,
                    parse_mode="HTML",
                    reply_markup=create_scoreboard_keyboard(),
                )

            except Exception as e:

                print(
                    f"❌ خطأ في إرسال دفتر النتائج "
                    f"بعد الخمس انتصارات: {e}"
                )

        # -------------------------------------------------
        # الانتقال للسؤال التالي
        # -------------------------------------------------

        game[
            "question_index"
        ] += 1

        if game[
            "question_index"
        ] >= len(GAMES_LIST):

            game[
                "question_index"
            ] = 0


# =========================================================
# أزرار دفتر النتائج
# =========================================================

async def callback_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if not query:
        return

    data = query.data

    if not data:
        return

    if not query.message:
        return

    chat_id = query.message.chat_id

    # =====================================================
    # عرض دفتر النتائج
    # =====================================================

    if data == "show_scoreboard":

        scores = user_scores.get(
            chat_id,
            {}
        )

        if not scores:

            await query.answer(
                "📭 دفتر النتائج فارغ حتى الآن!",
                show_alert=True
            )

            return

        scoreboard_text = build_scoreboard_text(
            chat_id
        )

        try:

            await query.message.reply_text(
                scoreboard_text,
                parse_mode="HTML",
                reply_markup=create_scoreboard_keyboard(),
            )

        except Exception as e:

            print(
                f"❌ خطأ في عرض دفتر النتائج: {e}"
            )

        await query.answer()

        return

    # =====================================================
    # إغلاق دفتر النتائج
    # =====================================================

    if data == "close_score":

        try:

            await query.message.delete()

        except Exception:

            pass

        await query.answer()

        return

    # =====================================================
    # السابق / التالي
    # =====================================================

    if data in [
        "prev_score",
        "next_score"
    ]:

        await query.answer(
            "📊 جميع النتائج موجودة في دفتر النتائج الحالي.",
            show_alert=True
        )

        return


# =========================================================
# تسجيل Handlers
# =========================================================

def setup_game_handlers(app):

    # -----------------------------------------------------
    # بدء اللعبة فقط عند كتابة "غباش"
    # -----------------------------------------------------

    app.add_handler(
        MessageHandler(
            filters.Regex(
                r"^غباش$"
            ),
            start_game
        )
    )

    # -----------------------------------------------------
    # استقبال إجابات اللاعبين
    # -----------------------------------------------------

    app.add_handler(
        MessageHandler(
            filters.TEXT
            & (~filters.COMMAND),
            handle_game_message
        )
    )

    # -----------------------------------------------------
    # أزرار دفتر النتائج
    # -----------------------------------------------------

    app.add_handler(
        CallbackQueryHandler(
            callback_handler,
            pattern=(
                r"^(show_scoreboard|"
                r"close_score|"
                r"prev_score|"
                r"next_score)$"
            )
        )
    )

    print(
        "✅ تم تحميل نظام لعبة الغباش بنجاح."
    )
