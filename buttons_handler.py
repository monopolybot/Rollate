# buttons_handler.py
# نظام الأزرار الملكي المطور للـ 21 مجموعة مع خيارات (ناقص / زائد) لتنسيق التبادل

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database_handler import update_user_cards, find_matches

# استيراد الأسماء الصحيحة مباشرة من ملف cards_engine لضمان عدم وجود أي تناقض
from cards_engine import ALBUMS_DATA

# 1. عرض المجموعات الـ 21 الأساسية
async def start_card_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        message = query.message
    else:
        message = update.message

    keyboard = []
    row = []
    for album_id in ALBUMS_DATA.keys():
        row.append(InlineKeyboardButton(f"📁 مجموعة {album_id}", callback_data=f"select_album_{album_id}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("❌ إغلاق القائمة", callback_data="close_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = "👑 **نظام التبادل الملكي للبطاقات**\n\nاختر المجموعة المطلوبة لتحديد البطاقات (ناقصة أو زائدة):"
    
    if query:
        try:
            await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")
        except Exception:
            await context.bot.send_message(chat_id=message.chat_id, text=text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# التعامل مع الأزرار والخيارات
async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user = query.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else user.first_name

    # عند اختيار مجموعة معينة -> عرض بطاقاتها مع خيارات (أحتاجه / متوفر لدي)
    if data.startswith("select_album_"):
        album_id = int(data.replace("select_album_", ""))
        cards = ALBUMS_DATA.get(album_id)
        
        if not cards:
            return

        keyboard = []
        for card in cards:
            # صف لكل بطاقة يحتوي على اسم البطاقة وزرين (أحتاجه / متوفر لدي)
            keyboard.append([InlineKeyboardButton(f"🎴 {card}", callback_data="noop")]) # عنوان البطاقة غير قابل للضغط
            keyboard.append([
                InlineKeyboardButton("❌ أحتاجه (ناقص)", callback_data=f"status_need_{album_id}_{card}"),
                InlineKeyboardButton("✅ متوفر (زائد)", callback_data=f"status_have_{album_id}_{card}")
            ])
        
        # زر الرجوع الفعال الآمن (يتم تعديل الرسالة بدلاً من حذفها لمنع الخروج المفاجئ)
        keyboard.append([InlineKeyboardButton("🔙 العودة للمجموعات", callback_data="back_to_albums")])
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            await query.message.edit_text(
                f"📌 **مجموعة رقم {album_id}**\n\nحدد حالة كل بطاقة (ناقصة للبحث أو زائدة للتبادل):",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        except Exception:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"📌 **مجموعة رقم {album_id}**\n\nحدد حالة كل بطاقة (ناقصة للبحث أو زائدة للتبادل):",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )

    # عند اختيار حالة البطاقة (ناقص أو زائد)
    elif data.startswith("status_need_") or data.startswith("status_have_"):
        parts = data.split("_", 3)
        status_type = parts[1] # need أو have
        album_id = parts[2]
        card_name = parts[3] if len(parts) > 3 else "بطاقة"
        
        status_text = "أحتاجه (ناقص)" if status_type == "need" else "متوفر لدي (زائد)"
        
        # حفظ الحالة في قاعدة البيانات
        update_user_cards(user_id, username, [{"card": card_name, "status": status_type, "album": album_id}])
        
        # البحث عن توافقات فورية وإرسال المنشن الحقيقي بالـ ID
        matches = find_matches()
        for match in matches:
            for item in match.get("cards", []):
                giver_name = item["giver_name"]
                giver_id = item["giver_id"]
                receiver_name = item["receiver_name"]
                receiver_id = item["receiver_id"]
                card_title = item["card"]
                
                # التأكد أن العضو الحالي هو أحد طرفي التبادل لتجنب تكرار الرسائل غير الضرورية
                if user_id in [giver_id, receiver_id]:
                    await context.bot.send_message(
                        chat_id=query.message.chat_id,
                        text=(
                            f"🤝 <b>تـنـسـيـق تـلـقـائي لـلـتـبـادل الـمـلـكـي!</b> 🤝\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"🎁 <b>المتبرع (يملك الكرت زائد):</b> <a href='tg://user?id={giver_id}'><b>{giver_name}</b></a>\n"
                            f"🎯 <b>المستلم (يحتاج الكرت ناقص):</b> <a href='tg://user?id={receiver_id}'><b>{receiver_name}</b></a>\n\n"
                            f"🎴 <b>البطاقة المتوافقة:</b> <code>{card_title}</code>\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"⚡ <i>الرجاء التنسيق بينكما لإتمام التبادل بنجاح!</i>"
                        ),
                        parse_mode="HTML"
                    )

        await query.answer(f"✅ تم تسجيل ({card_name}) كـ [{status_text}] بنجاح!", show_alert=True)

    elif data == "noop":
        await query.answer("هذا عنوان البطاقة، استخدم الأزرار بالأسفل لتحديد حالتها 👇", show_alert=False)

    elif data == "back_to_albums":
        # إعادة توجيه نظيفة لعرض القائمة الرئيسية مباشرة دون أخطاء أو خروج مفاجئ
        await start_card_selection(update, context)

    elif data == "close_menu":
        try:
            await query.message.delete()
        except Exception:
            pass
