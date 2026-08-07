import os
import logging
import google.generativeai as genai
from telethon import events

logger = logging.getLogger(__name__)

# إعداد مفتاح Gemini
genai.configure(api_key="AIzaSyAMpzwY1Gt4-NTtTf5r9n8MPc1vk37ZMrE")
model = genai.GenerativeModel('gemini-1.5-flash')

# المجموعات المعتمدة حصرياً
ALLOWED_GROUPS = [
    -1004432647304,
    -1002052564369,
    -1004477090207,
    -1004290639724
]

def setup_vision_handler(client):
    """
    معالج الصور الجديد للبطاقات - يعمل في ملف منفصل لتأمين النظام القديم.
    """
    @client.on(events.NewMessage(chats=ALLOWED_GROUPS, incoming=True))
    async def handle_incoming_screenshot(event):
        if event.photo:
            processing_msg = await event.reply("🔍 **جارٍ تحليل لقطة الشاشة باستخدام الذكاء الاصطناعي.. ثوانٍ المعدودات!**")
            
            # التأكد من وجود مجلد التحميل
            if not os.path.exists("downloads"):
                os.makedirs("downloads")
                
            # تحميل الصورة مؤقتاً
            path = await event.download_media(file="downloads/")
            
            try:
                with open(path, "rb") as image_file:
                    img_data = image_file.read()
                
                # إرسال الصورة لنموذج الرؤية لتحليل الزوائد والنواقص
                response = model.generate_content([
                    "استخرج أسماء البطاقات الموجودة في هذه الصورة بدقة. صنفها بوضوح إلى: بطاقات زائدة (التي تحتوي على علامة +1 أو أكثر) وبطاقات ناقصة (الأماكن الفارغة أو المطلوبة).",
                    {"mime_type": "image/jpeg", "data": img_data}
                ])
                
                await processing_msg.edit(f"✅ **نتائج تحليل البطاقات:**\n\n{response.text}")
            
            except Exception as e:
                logger.error(f"Error analyzing image: {e}")
                await processing_msg.edit("⚠️ حدث خطأ أثناء تحليل الصورة، يرجى المحاولة مرة أخرى.")
            
            # حذف الصورة المؤقتة من السيرفر
            if path and os.path.exists(path):
                os.remove(path)
