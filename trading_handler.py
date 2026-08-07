# trading_handler.py
# معالج الرسائل والصور لتنسيق التبادل التلقائي بين الأعضاء بذكاء وسرعة

import os
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
    if not message or not message.photo:
        return

    chat_id = message.chat_id
    
    # التأكد من أن الرسالة في إحدى المجموعات المسموحة لديك
    if ALLOWED_GROUPS and str(chat_id) not in [str(g) for g in ALLOWED_GROUPS]:
        return

    user = message.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else user.first_name

    try:
        # إرسال تنبيه خفيف وسريع يفيد ببدء المعالجة بدون إحداث ضغط على التيليجرام
        status_msg = await message.reply_text("🔍 جاري قراءة وتحليل الألبوم تلقائياً...")

        # تنزيل الصورة المعالجة مؤقتاً
        photo_file = await message.photo[-1].get_file()
        os.makedirs("temp_images", exist_ok=True)
        image_path = f"temp_images/{user_id}_{message.message_id}.jpg"
        await photo_file.download_to_drive(image_path)

        # معالجة الصورة واستخراج البطاقات عبر pytesseract
        result = await process_user_album_image(image_path)

        if result["status"] == "error":
            await status_msg.edit_text("❌ حدث خطأ أثناء تحليل الصورة، يرجى المحاولة لاحقاً.")
            return

        cards = result.get("cards", [])
        if not cards:
            await status_msg.edit_text("⚠️ لم يتم التعرف على أي بطاقات واضحة في الصورة، تأكد من وضوح الألبوم.")
            return

        # تحديث قاعدة بيانات العضو بالبطاقات المكتشفة
        update_user_cards(user_id, username, cards)

        # البحث عن تطابقات مع بقية الأعضاء
        matches = find_matches()

        # تحديث رسالة البوت بنجاح العملية
        await status_msg.edit_text(f"✅ تم تسجيل بطاقاتك بنجاح! (تم رصد {len(cards)} بطاقة). جاري البحث عن تطابقات...")

        # التحقق مما إذا كان هناك تطابق يتطلب المنشن التلقائي
        match_found = False
        for match in matches:
            if username in [match.get("user1"), match.get("user2")]:
                other_user = match["user2"] if match["user1"] == username else match["user1"]
                matched_items = ", ".join(match.get("cards", []))
                
                match_found = True
                # إرسال رسالة التوافق والمنشن التلقائي بأسلوب راقي
                await message.reply_text(
                    f"🤝 **تنسيق تلقائي للتبادل الملكي!**\n\n"
                    f"✨ تم رصد توافق بين العضو: {username}\n"
                    f"✨ والطرف الآخر: {other_user}\n\n"
                    f"📌 **البطاقات المتوافقة:** [{matched_items}]\n\n"
                    f"الرجاء التنسيق مع الادارة لإتمام التبادل بنجاح!"
                )

        if not match_found:
            # رسالة هادئة في حال عدم وجود تطابق فوري بانتظار دخول أعضاء جدد
            pass

    except Exception as e:
        # التعامل مع أخطاء التيليجرام أو الضغط لتفادي توقف البوت
        print(f"Error in handle_album_photo: {e}")
