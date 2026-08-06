# trading_handler.py
# معالج الرسائل والصور لتنسيق التبادل التلقائي بين الأعضاء

from telegram import Update
from telegram.ext import ContextTypes
from image_processor import process_user_album_image
from database_handler import update_user_cards, find_matches
from config import ALLOWED_GROUPS  # استيراد المجموعات المسموحة لديك

async def handle_album_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    معالجة الصور المرسلة تلقائياً بدون أي أوامر، والبحث عن تطابقات ومنشن الأعضاء
    """
    message = update.message
    chat_id = message.chat_id
    
    # التأكد من أن الرسالة في إحدى المجموعات المسموحة لديك
    if ALLOWED_GROUPS and str(chat_id) not in [str(g) for g in ALLOWED_GROUPS]:
        return

    # التحقق من أن الرسالة تحتوي على صورة
    if not message.photo:
        return

    user = message.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else user.first_name

    # إعلام العضو بأن البوت يقرأ الصورة في الخلفية
    status_msg = await message.reply_text("🔍 جاري قراءة وتحليل الألبوم تلقائياً...")

    # تنزيل الصورة المعالجة مؤقتاً
    photo_file = await message.photo[-1].get_file()
    image_path = f"temp_{user_id}.jpg"
    await photo_file.download_to_drive(image_path)

    # معالجة الصورة واستخراج البطاقات
    result = await process_user_album_image(image_path)

    if result["status"] == "error":
        await status_msg.edit_text("❌ حدث خطأ أثناء تحليل الصورة، يرجى المحاولة لاحقاً.")
        return

    cards = result["cards"]
    if not cards:
        await status_msg.edit_text("⚠️ لم يتم التعرف على أي بطاقات واضحة في الصورة، تأكد من وضوح الألبوم.")
        return

    # استخراج أسماء البطاقات فقط للتخزين
    card_names = [c["card"] for c in cards]

    # تحديث قاعدة بيانات العضو
    update_user_cards(user_id, username, card_names)

    # البحث عن تطابقات مع بقية الأعضاء
    matches = find_matches()

    # تحديث رسالة البوت بنجاح العملية
    await status_msg.edit_text(f"✅ تم تسجيل بطاقاتك بنجاح! (تم رصد {len(card_names)} بطاقة). جاري مطابقتها مع الأعضاء...")

    # التحقق مما إذا كان هناك تطابق يتطلب المنشن التلقائي
    for match in matches:
        if username in [match["user1"], match["user2"]]:
            other_user = match["user2"] if match["user1"] == username else match["user1"]
            matched_items = ", ".join(match["cards"])
            
            # إرسال رسالة المنشن التلقائي بين الطرفين في المجموعة
            await message.reply_text(
                f"🤝 **تنسيق تلقائي للتبادل!**\n"
                f"وجدنا تطابقاً بين العضو {username} والعضو {other_user}\n"
                f"📌 البطاقات المتوافقة: [{matched_items}]\n"
                f"الرجاء الرد بواسطة الادارة لإتمام التبادل بنجاح!"
            )
