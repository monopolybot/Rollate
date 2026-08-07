import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
from config import ALLOWED_GROUPS

logger = logging.getLogger(__name__)

# إعداد مفتاح Gemini للرؤية البصرية الذكية
genai.configure(api_key="AIzaSyAMpzwY1Gt4-NTtTf5r9n8MPc1vk37ZMrE")
model = genai.GenerativeModel('gemini-1.5-flash')

# قاعدة بيانات مؤقتة في الذاكرة لتخزين بطاقات الأعضاء لكل جروب
group_cards_database = {}

async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in ALLOWED_GROUPS:
        return

    # التحقق مما إذا كانت الرسالة تحتوي على صورة
    if update.message and update.message.photo:
        user = update.effective_user
        u_id = user.id
        u_name = user.first_name

        processing_msg = await update.message.reply_text(
            "👑 **مـمـلكـة مـونـوبـولـي** 👑\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "🔍 **جارٍ تحليل لقطة الشاشة واستخراج البطاقات بالذكاء الاصطناعي.. ثوانٍ معدودات!**", 
            parse_mode='HTML'
        )
        
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
            
        # تحميل أعلى دقة للصورة المرسلة
        photo_file = await update.message.photo[-1].get_file()
        path = os.path.join("downloads", f"{u_id}_{chat_id}.jpg")
        await photo_file.download_to_drive(path)
        
        try:
            with open(path, "rb") as image_file:
                img_data = image_file.read()
            
            prompt = (
                "قم بتحليل لقطة شاشة لعبة مونوبولي هذه بدقة بالغة. "
                "أعطني النتيجة مقسمة حصرياً إلى قسمين: "
                "1. الزوائد: (اكتب كل بطاقة زائدة في سطر جديد مسبوقة بـ - وتحديداً البطاقات التي تحتوي على علامة +1 أو أكثر). "
                "2. النواقص: (اكتب كل بطاقة ناقصة أو مكان فارغ في سطر جديد مسبوقة بـ -). "
                "لا تقم بإضافة تفاصيل طويلة، فقط أطراف الأسماء أو أسماء البطاقات واضحة."
            )
            
            response = model.generate_content([
                prompt,
                {"mime_type": "image/jpeg", "data": img_data}
            ])
            
            ai_text = response.text

            surplus_cards = []
            missing_cards = []
            current_section = None
            
            for line in ai_text.split('\n'):
                line_lower = line.lower()
                if 'زائد' in line_lower or 'الزوائد' in line_lower or 'surplus' in line_lower:
                    current_section = 'surplus'
                    continue
                elif 'ناقص' in line_lower or 'النواقص' in line_lower or 'missing' in line_lower:
                    current_section = 'missing'
                    continue
                
                if line.strip().startswith('-'):
                    card_name = line.strip().lstrip('- ').strip()
                    if card_name:
                        if current_section == 'surplus':
                            surplus_cards.append(card_name)
                        elif current_section == 'missing':
                            missing_cards.append(card_name)

            if chat_id not in group_cards_database:
                group_cards_database[chat_id] = {}

            # قائمة لجمع التوافقات الفريدة لمنع أي تكرار
            unique_matches = []
            
            for other_id, other_data in group_cards_database[chat_id].items():
                if other_id != u_id:
                    # 1. ما يملكه الآخر ويزيد عنه ويحتاجه العضو الحالي
                    common_cards_giver = list(set(other_data['surplus']).intersection(set(missing_cards)))
                    if common_cards_giver:
                        cards_str = ", ".join([f"<code>{c}</code>" for c in common_cards_giver])
                        match_msg = (
                            f"🤝 <b>تـنـسـيـق تـلـقـائي لـلـتـبـادل الـمـلـكـي!</b> 🤝\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"🎁 <b>المتبرع (يملك الكرت زائد):</b> <a href='tg://user?id={other_id}'><b>{other_data['name']}</b></a>\n"
                            f"🎯 <b>المستلم (يحتاج الكرت ناقص):</b> <a href='tg://user?id={u_id}'><b>{u_name}</b></a>\n\n"
                            f"🎴 <b>البطاقات المتوافقة:</b> {cards_str}\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"⚡ <i>الرجاء التنسيق مع الادارة لإتمام التبادل بنجاح!</i>"
                        )
                        if match_msg not in unique_matches:
                            unique_matches.append(match_msg)

                    # 2. ما يملكه العضو الحالي ويزيد عنه ويحتاجه الآخر
                    common_cards_receiver = list(set(surplus_cards).intersection(set(other_data['missing'])))
                    if common_cards_receiver:
                        cards_str = ", ".join([f"<code>{c}</code>" for c in common_cards_receiver])
                        match_msg = (
                            f"🤝 <b>تـنـسـيـق تـلـقـائي لـلـتـبـادل الـمـلـكـي!</b> 🤝\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"🎁 <b>المتبرع (يملك الكرت زائد):</b> <a href='tg://user?id={u_id}'><b>{u_name}</b></a>\n"
                            f"🎯 <b>المستلم (يحتاج الكرت ناقص):</b> <a href='tg://user?id={other_id}'><b>{other_data['name']}</b></a>\n\n"
                            f"🎴 <b>البطاقات المتوافقة:</b> {cards_str}\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"⚡ <i>الرجاء التنسيق مع الادارة لإتمام التبادل بنجاح!</i>"
                        )
                        if match_msg not in unique_matches:
                            unique_matches.append(match_msg)

            # تحديث بيانات العضو الحالي في الذاكرة
            group_cards_database[chat_id][u_id] = {
                "name": u_name,
                "surplus": surplus_cards,
                "missing": missing_cards
            }

            base_response = (
                f"👑 **تـحـلـيـل بـطـاقـات العضو {u_name}**\n"
                f"━━━━━━━━━━━━━━━━━━━\n\n"
                f"{ai_text}"
            )
            
            await processing_msg.edit_text(base_response, parse_mode='HTML')

            # إرسال رسائل التوافق الفريدة فقط بدون أي تكرار
            for msg in unique_matches:
                await update.message.reply_text(msg, parse_mode='HTML')
        
        except Exception as e:
            logger.error(f"Error analyzing image for user {u_id}: {e}")
            await processing_msg.edit_text("⚠️ **حدث خطأ ملكي أثناء معالجة الصورة، يرجى التأكد من وضوحها وإعادة إرسالها.**", parse_mode='HTML')
        
        if path and os.path.exists(path):
            os.remove(path)

def setup_vision_handler(app):
    app.add_handler(MessageHandler(filters.PHOTO & filters.Chat(ALLOWED_GROUPS), handle_screenshot))
