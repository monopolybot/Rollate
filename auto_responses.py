# auto_responses.py
import asyncio
from datetime import datetime
import pytz
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

# ضع هنا معرف المجموعة الخاصة بك
TARGET_GROUP_ID = -1002695848824

rotation_indexes = {
    "goodnight": 0,
    "morning": 0,
    "evening": 0
}

async def handle_auto_responses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip().lower()

    # 1. المعرف الأول: تصبحوا على خير
    if any(word in text for word in ["تصبحوا على خير", "تصبحون على خير"]):
        videos = [
            "BAACAgQAAxkBAAMlapikxmvp2Lqgb2aDzy-QbG7o_c4AApkgAAIUlslQQVD5ARgW5YM9BA",
            "BAACAgQAAxkBAAMqapimyy8jEyUTAu2GIOf9EuBeBZcAAlYiAAKiYchQ8zwQ9K4owac9BA"
        ]
        idx = rotation_indexes["goodnight"]
        await update.message.reply_video(video=videos[idx])
        rotation_indexes["goodnight"] = (idx + 1) % len(videos)

    # 2. المعرف الثاني: السلام عليكم
    elif any(word in text for word in ["السلام عليكم", "السلام", "سلام عليكم"]):
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

    # كلمة سلام المفردة
    elif text == "سلام":
        video_id = "BAACAgQAAxkBAAMoapimHFS2kS1j3lojepDovQ_a5d4AAlUiAAKiYchQe5xlUj_65Nw9BA"
        await update.message.reply_video(video=video_id)

    # 5. الردود النصية للمساعدة (بخاط عريض)
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

# --- نظام الجدولة الذاتي لتوقيت الأردن ---
async def schedule_loop(application):
    jordans_tz = pytz.timezone('Asia/Amman')
    
    while True:
        try:
            now = datetime.now(jordans_tz)
            current_hour = now.hour
            current_minute = now.minute

            # أذكار الصباح (6:00 صباحاً و 10:00 صباحاً)
            if current_minute == 0:
                if current_hour == 6 or current_hour == 10:
                    msg = "<b>يا شعب مونوبولي العظيم</b>\n\n<b>حان الان موعد اذكار الصباح</b>\n\n<b>لا تنسونا من صالح دعائكم</b>"
                    await application.bot.send_message(chat_id=TARGET_GROUP_ID, text=msg, parse_mode='HTML')
                    await asyncio.sleep(60) # الانتظار دقيقة لمنع التكرار في نفس الساعة

                # أذكار المساء (8:00 مساءً و 11:00 ليلاً)
                elif current_hour == 20 or current_hour == 23:
                    msg = "<b>يا شعب مونوبولي العظيم</b>\n\n<b>حان الان موعد اذكار المساء</b>\n\n<b>لا تنسونا من صالح دعائكم</b>"
                    await application.bot.send_message(chat_id=TARGET_GROUP_ID, text=msg, parse_mode='HTML')
                    await asyncio.sleep(60)

                # مواعيد الصلاة التقريبية بتوقيت الأردن
                prayer_times = {
                    (4, 45): "الفجر",
                    (12, 30): "الظهر",
                    (15, 45): "العصر",
                    (19, 15): "المغرب",
                    (20, 45): "العشاء"
                }
                
                if (current_hour, current_minute) in prayer_times:
                    p_name = prayer_times[(current_hour, current_minute)]
                    msg = f"<b>يا شعب مونوبولي العظيم</b>\n\n<b>حسب التوقيت المحلي للمملكة الأردنية الهاشمية</b>\n\n<b>حان الان موعد صلاة {p_name}</b>"
                    await application.bot.send_message(chat_id=TARGET_GROUP_ID, text=msg, parse_mode='HTML')
                    await asyncio.sleep(60)

        except Exception as e:
            print(f"خطأ في حلقة الجدولة: {e}")
            
        # فحص الوقت كل 30 ثانية
        await asyncio.sleep(30)

def register_auto_responses(application):
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_auto_responses))
    # تشغيل حلقة الجدولة بشكل غير متزامن في الخلفية عند بدء البوت
    asyncio.create_task(schedule_loop(application))
