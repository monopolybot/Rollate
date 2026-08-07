# trading_handler.py
# معالج الرسائل والصور لتنسيق التبادل التلقائي بين الأعضاء بأسلوب ملكي راقي

import os
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from image_processor import process_user_album_image
from database_handler import update_user_cards, find_matches
from config import ALLOWED_GROUPS

async def handle_album_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.photo:
        return

    chat_id = message.chat_id
    if ALLOWED_GROUPS and str(chat_id) not in [str(g) for g in ALLOWED_GROUPS]:
        return

    user = message.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else user.first_name

    try:
        await asyncio.sleep(0.5)
        status_msg = await message.reply_text("🔍 جاري قراءة وتحليل الألبوم تلقائياً...")

        # تحميل الصورة المؤقتة بأمان
        photo_file = await message.photo[-1].get_file()
        os.makedirs("temp_images", exist_ok=True)
        image_path = f"temp_images/{user_id}_{message.message_id}.jpg"
        await photo_file.download_to_drive(image_path)

        # معالجة الصورة عبر المعالج الآمن
        result = await process_user_album_image(image_path)
        
        # تنظيف الصورة فوراً بعد المعالجة لتوفير الذاكرة
        if os.path.exists(image_path):
            os.remove(image_path)

        if result.get("status") == "error":
            await status_msg.edit_text("❌ حدث خطأ أثناء تحليل الصورة، يرجى المحاولة لاحقاً.")
            return

        raw_cards = result.get("cards", [])
        
        # استخراج أسماء البطاقات بشكل آمن سواء كانت نصوص أو قواميس
        card_names = []
        for c in raw_cards:
            if isinstance(c, dict):
                card_names.append(c.get("card", "Unknown"))
            else:
                card_names.append(str(c))

        if not card_names:
            await status_msg.edit_text("⚠️ لم يتم التعرف على أي بطاقات واضحة في الصورة.")
            return

        # تحديث قاعدة البيانات والبحث عن التطابقات
        update_user_cards(user_id, username, card_names)
        matches = find_matches()

        await status_msg.edit_text(f"✅ تم تسجيل بطاقاتك بنجاح! ({len(card_names)} بطاقة).")

        for match in matches:
            if username in [match.get("user1"), match.get("user2")]:
                other_user = match["user2"] if match["user1"] == username else match["user1"]
                
                matched_raw = match.get("cards", [])
                matched_names = [m.get("card", str(m)) if isinstance(m, dict) else str(m) for m in matched_raw]
                matched_items = ", ".join(matched_names)
                
                await asyncio.sleep(0.3)
                
                # إرسال رسالة التوافق والمنشن التلقائي بأسلوب راقي
                await message.reply_text(
                    f"🤝 **تنسيق تلقائي للتبادل الملكي!**\n\n"
                    f"✨ تم رصد توافق بين العضو: {username}\n"
                    f"✨ والطرف الآخر: {other_user}\n\n"
                    f"📌 **البطاقات المتوافقة:** [{matched_items}]\n\n"
                    f"الرجاء التنسيق مع الادارة لإتمام التبادل بنجاح!"
                )

    except Exception as e:
        print(f"Error in handle_album_photo: {e}")
        try:
            await message.reply_text("❌ حدث خطأ تقني مؤقت أثناء استقبال الصورة، يرجى إعادة إرسالها.")
        except:
            pass
