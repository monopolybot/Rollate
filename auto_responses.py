# auto_responses.py
import asyncio
import json
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

# قائمة المجموعات المسموحة للنشر التلقائي
ALLOWED_GROUPS = [
    -1004432647304,
    -1002052564369,
    -1004477090207,
    -1004400057155
]

AMMAN_TZ = ZoneInfo('Asia/Amman')

cached_prayer_times = {}
last_fetched_date = None

def fetch_amman_prayer_times():
    """جلب مواقيت الصلاة الدقيقة لمدينة عمان - الأردن لليوم الحالي"""
    global cached_prayer_times, last_fetched_date
    today_str = datetime.now(AMMAN_TZ).strftime('%d-%m-%Y')
    
    if last_fetched_date == today_str and cached_prayer_times:
        return cached_prayer_times

    try:
        url = "http://api.aladhan.com/v1/timingsByCity?city=Amman&country=Jordan&method=5"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            timings = data['data']['timings']
            cached_prayer_times = {
                "الفجر": timings['Fajr'][:5],
                "الظهر": timings['Dhuhr'][:5],
                "العصر": timings['Asr'][:5],
                "المغرب": timings['Maghrib'][:5],
                "العشاء": timings['Isha'][:5]
            }
            last_fetched_date = today_str
    except Exception as e:
        print(f"خطأ في جلب مواقيت الصلاة: {e}")
    
    return cached_prayer_times

async def schedule_loop(application):
    sent_today = {"morning_6": False, "morning_10": False, "evening_20": False, "evening_23": False}
    sent_prayers = {}
    last_date = ""

    while True:
        try:
            now = datetime.now(AMMAN_TZ)
            current_date = now.strftime('%Y-%m-%d')
            current_time_str = now.strftime('%H:%M')

            if last_date != current_date:
                last_date = current_date
                sent_today = {k: False for k in sent_today}
                sent_prayers = {}

            # دوال إرسال الرسالة لجميع المجموعات المسموحة دفعة واحدة
            async def broadcast(message_text):
                for chat_id in ALLOWED_GROUPS:
                    try:
                        await application.bot.send_message(chat_id=chat_id, text=message_text, parse_mode='HTML')
                    except Exception as e:
                        print(f"فشل الإرسال للمجموعة {chat_id}: {e}")

            # أذكار الصباح (6:00 صباحاً)
            if current_time_str == "06:00" and not sent_today["morning_6"]:
                msg = (
                    "<b>👑 يا شعب مونوبولي العظيم 👑</b>\n\n"
                    "<b>☀️ حان الان موعد أذكار الصباح ☀️</b>\n\n"
                    "<b>لا تنسونا من صالح دعائكم</b>"
                )
                await broadcast(msg)
                sent_today["morning_6"] = True

            # أذكار الصباح (10:00 صباحاً)
            elif current_time_str == "10:00" and not sent_today["morning_10"]:
                msg = (
                    "<b>👑 يا شعب مونوبولي العظيم 👑</b>\n\n"
                    "<b>☀️ حان الان موعد أذكار الصباح ☀️</b>\n\n"
                    "<b>لا تنسونا من صالح دعائكم</b>"
                )
                await broadcast(msg)
                sent_today["morning_10"] = True

            # أذكار المساء (8:00 مساءً)
            elif current_time_str == "20:00" and not sent_today["evening_20"]:
                msg = (
                    "<b>👑 يا شعب مونوبولي العظيم 👑</b>\n\n"
                    "<b>🌙 حان الان موعد أذكار المساء 🌙</b>\n\n"
                    "<b>لا تنسونا من صالح دعائكم</b>"
                )
                await broadcast(msg)
                sent_today["evening_20"] = True

            # أذكار المساء (11:00 ليلاً)
            elif current_time_str == "23:00" and not sent_today["evening_23"]:
                msg = (
                    "<b>👑 يا شعب مونوبولي العظيم 👑</b>\n\n"
                    "<b>🌙 حان الان موعد أذكار المساء 🌙</b>\n\n"
                    "<b>لا تنسونا من صالح دعائكم</b>"
                )
                await broadcast(msg)
                sent_today["evening_23"] = True

            # مواعيد الصلاة الدقيقة 100%
            timings = fetch_amman_prayer_times()
            for p_name, p_time in timings.items():
                if current_time_str == p_time and not sent_prayers.get(p_name, False):
                    msg = (
                        "<b>👑 يا شعب مونوبولي العظيم 👑</b>\n\n"
                        "<b>حسب التوقيت المحلي للمملكة الأردنية الهاشمية</b>\n\n"
                        f"<b>🕌 حان الان موعد صلاة {p_name} 🕌</b>"
                    )
                    await broadcast(msg)
                    sent_prayers[p_name] = True

        except Exception as e:
            print(f"خطأ في حلقة الجدولة: {e}")

        await asyncio.sleep(30)

def register_auto_responses(application):
    pass
