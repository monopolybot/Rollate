# auto_responses.py
import random
import asyncio
from datetime import datetime
import pytz
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

# متغيرات لتتبع المداورة بين المقاطع (للمجموعات)
rotation_indexes = {
    "goodnight": 0,
    "morning": 0,
    "evening": 0
}

async def handle_auto_responses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    # تجاهل الرسائل في الخاص إذا أردت تطبيقها حصرياً في المجموعات (أو اتركها تعمل للجميع)
    chat_id = update.effective_chat.id
    text = update.message.text.strip().lower()

    # 1. المعرف الأول: تصبحوا على خير / سلام
    if any(word in text for word in ["تصبحوا على خير", "تصبحون على خير", "سلام"]):
        videos = [
            "BAACAgQAAxkBAAMlapikxmvp2Lqgb2aDzy-QbG7o_c4AApkgAAIUlslQQVD5ARgW5YM9BA",
            "BAACAgQAAxkBAAMqapimyy8jEyUTAu2GIOf9EuBeBZcAAlYiAAKiYchQ8zwQ9K4owac9BA"
        ]
        idx = rotation_indexes["goodnight"]
        await update.message.reply_video(video=videos[idx])
        rotation_indexes["goodnight"] = (idx + 1) % len(videos)

    # 2. المعرف الثاني: السلام عليكم / سلام عليكم
    elif any(word in text for word in ["السلام عليكم", "السلام", "سلام عليكم", "سلام"]):
        # ملاحظة: كلمة "سلام" مكررة مع المعرف الأول، سيتم مطابقتها هنا أو دمجها حسب الرغبة
        video_id = "BAACAgQAAxkBAAMoapimHFS2kS1j3lojepDovQ_a5d4AAlUiAAKiYchQe5xlUj_65Nw9BA"
        await update.message.reply_video(video=video_id)

    # 3. المعرف الثالث: صباح الخير / صباحكم / صباح النور (بالمداورة بين 3 مقاطع)
    elif any(word in text for word in ["صباح الخير", "صباحكم", "صباح النور"]):
        videos = [
            "BAACAgQAAxkBAAMsapinDR4uqZvycOwYxLYBaeRuU9gAAlciAAKiYchQIb6R77dHRVQ9BA",
            "BAACAgQAAxkBAAMyapior0SYvfQFkA9GlX52XR0OphgAAl0iAAKiYchQ34PP6SyXy8A9BA",
            "BAACAgQAAxkBAAMuapin_cV97tjomZc1VEtXoNOxc1EAAloiAAKiYchQle1xx7TgpPQ9BA"
        ]
        idx = rotation_indexes["morning"]
        await update.message.reply_video(video=videos[idx])
        rotation_indexes["morning"] = (idx + 1) % len(videos)

    # 4. المعرف الرابع: مساء الخير / مسا الخير / مساكم
    elif any(word in text for word in ["مساء الخير", "مسا الخير", "مساكم"]):
        videos = [
            "BAACAgQAAxkBAAMwapioLG2tiXC13-tWuX8X3jE-21EAAlsiAAKiYchQWl9wYsX9v3c9BA",
            "BAACAgQAAxkBAAMyapior0SYvfQFkA9GlX52XR0OphgAAl0iAAKiYchQ34PP6SyXy8A9BA"
        ]
        idx = rotation_indexes["evening"]
        await update.message.reply_video(video=videos[idx])
        rotation_indexes["evening"] = (idx + 1) % len(videos)

    # 5. الردود النصية للمساعدة
    elif any(word in text for word in ["مساعدة", "ساعدوني", "مساعده", "ساعدني"]):
        reply_text = (
            "<b>عـزيـزي المـواطـن</b>\n\n"
            "<b>عـزيـزي المحـتـرم</b>\n\n"
            "<b>اذا اردت المساعدة فعليك رد الجميل والمعروف لاعضاء هذه المجموعة</b>\n\n"
            "<b>اذا حصلت على مساعدة مجانية</b>\n"
            "<b>نرجوا منك رد هذه المساعدة لاي عضو اخر يحتاج لاي كرت او ملصق انت تملكه</b>\n\n"
            "<b>مثلما ادخلنا السرور الى قلبك</b>\n\n"
            "<b>كن شريكنا بادخال السرور الى قلب عضو اخر</b>\n\n"
            "<b>اذا كان انس لا يراك تاكد ان الله يراك</b>"
        )
        await update.message.reply_text(reply_text, parse_mode='HTML')

def register_auto_responses(application):
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_auto_responses))
