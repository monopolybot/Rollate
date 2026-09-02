# main.py
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import BOT_TOKEN, ALLOWED_GROUPS, OWNER_ID
from admin_handler import is_user_admin, can_stop_roulette
from roulette_engine import game_manager
from buttons_handler import start_card_selection, button_callback_handler
#from vision_engine import setup_vision_handler
from file_id_extractor import register_extractor_handler
from auto_responses import register_auto_responses

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # صمام الأمان: تجاهل التحديثات التي لا تحتوي على رسالة نصية
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    if chat_id not in ALLOWED_GROUPS: 
        return

    text = update.message.text.strip()
    u_id = update.effective_user.id
    u_name = update.effective_user.first_name

    # 1. أمر البداية (روليت)
    if text == "روليت":
        if await is_user_admin(update, context):
            if game_manager.is_active:
                await update.message.reply_text("⚠️ <b>عذراً!</b> هناك روليت قائمة بالفعل في هذه المجموعة.\nيجب إنهاء الجولة الحالية بكلمة <b>'تم'</b> أولاً.", parse_mode='HTML')
                return

            game_manager.is_active = True
            game_manager.starter_id = u_id
            await update.message.reply_text(
    "👑 <b>مـمـلكـة مـونـوبـولـي تـنـاديـكـم</b> 👑\n"
    "━━━━━━━━━━━━━━━━━━━\n"
    "🔥🔥 <b>اشـتـعـلـت حرب الـرولـيـت!</b> 🔥🔥\n\n"
    "⚡ <b>لـوائح الفوز تـنتظر الأبطال...</b>\n"
    "اكتب الآن كلمة: <b>'انا'</b> لتسجيل اسمك في قائمة المشاركين!",
    parse_mode='HTML'
)


    # 2. تسجيل الأعضاء (انا)
    elif text == "انا" and game_manager.is_active:
        game_manager.add_player(u_id, u_name)

    # 3. أمر النهاية (تم)
    elif text == "تم" and game_manager.is_active:
        if can_stop_roulette(u_id, game_manager.starter_id):
            await game_manager.run_elimination(update, context)

    # 4. فتح قائمة الألبومات والبطاقات الملكية (البوماتي)
    elif text in ["البوماتي", "البومات", "ابدأ"]:
        await start_card_selection(update, context)

if __name__ == '__main__':
    forced_token = BOT_TOKEN
    
    # بناء التطبيق مع تحديد مهلات اتصال واسعة لمنع أخطاء الـ Timeout نهائياً
    app = (
        ApplicationBuilder()
        .token(forced_token)
        .read_timeout(30)
        .write_timeout(30)
        .connect_timeout(30)
        .pool_timeout(30)
        .build()
    )
    
    # تسجيل الهاندلرز بالترتيب الصحيح
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    app.add_handler(CallbackQueryHandler(button_callback_handler))
    #setup_vision_handler(app)
    register_extractor_handler(app)
    register_auto_responses(app)
    
    # --- التعديل السحري والآمن لتشغيل الأذكار والصلاة فوراً مع إقلاع البوت ---
    async def post_init(application):
        import asyncio
        from auto_responses import schedule_loop
        asyncio.create_task(schedule_loop(application))
    
    app.post_init = post_init
    # ---------------------------------------------------------------------
    
    print("البوت يعمل الآن بنجاح بالتوكن المعتمد ومع نظام الأزرار الملكي وحماية الاتصال...")
    app.run_polling()
