import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
from config import ALLOWED_GROUPS

logger = logging.getLogger(__name__)

# إعداد مفتاح Gemini
genai.configure(api_key="AIzaSyAMpzwY1Gt4-NTtTf5r9n8MPc1vk37ZMrE")
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in ALLOWED_GROUPS:
        return

    # التحقق مما إذا كانت الرسالة تحتوي على صورة
    if update.message and update.message.photo:
        processing_msg = await update.message.reply_text("🔍 **جارٍ تحليل لقطة الشاشة باستخدام الذكاء الاصطناعي.. ثوانٍ المعدودات!**", parse_mode='HTML')
        
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
            
        # تحميل أطول دقة للصورة
        photo_file = await update.message.photo[-1].get_file()
        path = os.path.join("downloads", f"{update.message.from_user.id}.jpg")
        await photo_file.download_to_drive(path)
        
        try:
            with open(path, "rb") as image_file:
                img_data = image_file.read()
            
            response = model.generate_content([
                "استخرج أسماء البطاقات الموجودة في هذه الصورة بدقة. صنفها بوضوح إلى: بطاقات زائدة (التي تحتوي على علامة +1 أو أكثر) وبطاقات ناقصة (الأماكن الفارغة أو المطلوبة).",
                {"mime_type": "image/jpeg", "data": img_data}
            ])
            
            await processing_msg.edit_text(f"✅ **نتائج تحليل البطاقات:**\n\n{response.text}")
        
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            await processing_msg.edit_text("⚠️ حدث خطأ أثناء تحليل الصورة، يرجى المحاولة مرة أخرى.")
        
        if path and os.path.exists(path):
            os.remove(path)

def setup_vision_handler(app):
    # تسجيل الهاندلر للصور داخل المجموعات المسموحة فقط
    app.add_handler(MessageHandler(filters.PHOTO & filters.Chat(ALLOWED_GROUPS), handle_screenshot))
