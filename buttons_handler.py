# buttons_handler.py
# نظام الأزرار التفاعلية باللغة العربية للـ 21 مجموعة لتنسيق التبادل الملكي

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database_handler import update_user_cards, find_matches

# اعتماد الألبومات الـ 21 والأسماء الأصلية المعتمدة
ALBUMS_DATA = {
    1: ["الخيار", "طماطم", "جزر", "بصل", "بطاطس", "ذرة", "بازلاء", "باذنجان", "فلفل حلو"],
    2: ["تفاح", "موز", "برتقال", "فراولة", "عنب", "بطيخ", "أناناس", "كيوي", "مانجو"],
    3: ["خبز", "حليب", "بيض", "جبن", "زبدة", "عسل", "مربى", "قهوة", "شاي"],
    4: ["بذور الطماطم", "سماد عضوي", "سقي النبات", "أشعة الشمس", "مقص التقليم", "عربة اليد", "مجرفة صغيرة", "خرطوم المياه", "شتلات جديدة"],
    5: ["جرافة صغيرة", "جرار زراعي", "حصادة", "مخزن الحبوب", "طاحونة القمح", "بئر الماء", "سياج خشبي", "معلف الحيوانات", "طاحونة هواء"],
    6: ["بقرة حلوب", "خروف سمين", "دجاجة بياضة", "بطة صغيرة", "حصان قوي", "معزاة نشيطة", "أرانب صغيرة", "ديك رومي", "طيور الداجن"],
    7: ["زهور الأقحوان", "ورد جوري", "عباد الشمس", "توليب أحمر", "ياسمين أبيض", "زنبق ناصع", "أوركيد نادر", "نبتة الصبار", "ريحان عطري"],
    8: ["عش الطيور", "فراشة ملونة", "نحلة نشيطة", "خنفساء منقطة", "قنفذ صغير", "سنجاب شجج", "عصفور الدوري", "سلحفاة هادئة", "ضفدع البركة"],
    9: ["سلة الفواكه", "صندوق الخضار", "جرة الحليب", "كيس الدقيق", "زجاجة العسل", "طبق البيض", "ربطة الحطب", "فانوس قديم", "قبعة القش"],
    10: ["فأس حاد", "منشار خشبي", "مطرقة ثقيلة", "مفتاح ربط", "مقص حدائق", "حبل متين", "سلم طويل", "عربة نقل", "قفازات متينة"],
    11: ["الطحين", "بيض", "الألبان", "جبن", "خضروات", "الفواكه", "مكسرات", "عسل", "التوابل الخاصة"],
    12: ["لأجل العلم!", "الفضولي", "عصير الثنائي", "مكعبات الذرة", "المساعد الفريد", "الطائرة السحابية", "تجنّب الأفوكادو", "عباد الشمس المشرق", "البطيخ الأزرق"],
    13: ["نشاط النحل", "الخلية", "قرص العسل", "الغذاء المريح", "ابتعد!", "لا يُصدَّق!", "لسعة نحل", "إسعاف ومودّة", "مذاق العسل"],
    14: ["ممر الأقواس", "نافورة القرية", "المحطة التالية", "نكهة غريبة", "كعكة الجزر", "التقاط الصور", "ألف مبروك!", "رودي روت", "يوم العرض"],
    15: ["قيلولة البقر", "استجمام الخنازير", "صو صو!", "جدي للغاية", "لعب خشن", "كلب عامل", "مفيد للغاية", "مع القطيع", "قطف التفاح"],
    16: ["مناطق الظل", "قرويون أمريكيون", "حياة صامتة", "صورة مثالية", "تفاح فني", "صورة عائلية", "أجواء رعوية", "حفيف الذرة", "سعادة وبساطة"],
    17: ["لوازم السلططة", "سلة ممتلئة", "يقطينة عملاقة", "خم الدجاج", "الخيرات", "قرون الذرة", "مواد محفوظة", "مجموعة المخلل", "وقت الوليمة"],
    18: ["غسيل لامع", "خارج العمل", "متأمل", "حمام الوحل", "الراعي المثالي", "أحلى حلة", "حياة الشرفة", "عصرة ليمون", "ضوء القمر"],
    19: ["مزحة بين", "تحفة فنية", "فضائيون!", "الدليل", "المؤامرة", "الارتياب", "قبعة الألمنيوم", "كائن فضائي", "انطلت عليك"],
    20: ["تشوّق كبير", "كلاسيكيات", "صوف يأكل صوفا", "اختيار الأفضل", "جودة عالية", "اليقطينة الرائعة", "تم الهدم", "مع الفرقة", "الألعاب النارية"],
    21: ["ويلي كويوتي", "القط المرعوب", "رود رانر", "تويتي الكناري", "سيلفستر", "هيكتور", "هدية مشبوهة", "إلمر فد", "باغز باني"]
}

# أمر بدء التسجيل (يعرض المجموعات الـ 21)
async def start_card_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        message = query.message
    else:
        message = update.message

    keyboard = []
    # ترتيب الألبومات في أزرار (كل ألبومين في صف لتسهيل التصفح)
    row = []
    for album_id in ALBUMS_DATA.keys():
        row.append(InlineKeyboardButton(f"📁 المجموعة {album_id}", callback_data=f"select_album_{album_id}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("❌ إغلاق القائمة", callback_data="close_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = "👑 **نظام التبادل الملكي للبطاقات**\n\nالرجاء اختيار المجموعة المطلوبة لعرض بطاقاتها الحقيقية وتحديد ما تمتلكه:"
    
    if query:
        await message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# التعامل مع الضغط على الأزرار
async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user = query.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else user.first_name

    if data.startswith("select_album_"):
        album_id = int(data.replace("select_album_", ""))
        cards = ALBUMS_DATA.get(album_id)
        
        if not cards:
            await query.edit_text("⚠️ المجموعة غير موجودة.")
            return

        keyboard = []
        for card in cards:
            keyboard.append([InlineKeyboardButton(f"🎴 {card}", callback_data=f"get_card_{album_id}_{card}")])
        
        keyboard.append([InlineKeyboardButton("🔙 العودة للمجموعات", callback_data="back_to_albums")])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_text(
            f"📌 **مجموعة رقم {album_id}**\n\nاضغط على البطاقة لتسجيلها ضمن بطاقاتك المتوفرة:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    elif data.startswith("get_card_"):
        parts = data.split("_", 2)
        card_name = parts[2] if len(parts) > 2 else "بطاقة"
        
        # حفظ البطاقة الحقيقية في قاعدة البيانات
        update_user_cards(user_id, username, [card_name])
        
        # البحث عن تطابقات فورية
        matches = find_matches()

        for match in matches:
            if username in [match.get("user1"), match.get("user2")]:
                other_user = match["user2"] if match["user1"] == username else match["user1"]
                matched_raw = match.get("cards", [])
                matched_names = [str(m.get("card") if isinstance(m, dict) else m) for m in matched_raw]
                matched_items = ", ".join(matched_names)
                
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=(
                        f"🤝 **تنسيق تلقائي للتبادل الملكي!**\n\n"
                        f"✨ تم رصد توافق بين العضو: {username}\n"
                        f"✨ والطرف الآخر: {other_user}\n\n"
                        f"📌 **البطاقات المتوافقة:**\n`{matched_items}`\n\n"
                        f"الرجاء التنسيق مع الادارة لإتمام التبادل بنجاح!"
                    ),
                    parse_mode="Markdown"
                )

        await query.answer(f"✅ تم تسجيل بطاقة ({card_name}) بنجاح!", show_alert=True)

    elif data == "back_to_albums":
        await start_card_selection(update, context)

    elif data == "close_menu":
        await query.message.delete()
