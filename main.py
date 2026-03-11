from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, ALLOWED_GROUPS, OWNER_ID
from admin_handler import is_user_admin, can_stop_roulette
from roulette_engine import game_manager

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in ALLOWED_GROUPS: return

    text = update.message.text.strip()
    u_id = update.effective_user.id
    u_name = update.effective_user.first_name

    # 1. أمر البداية (روليت)
    if text == "روليت":
        if await is_user_admin(update, context):
            game_manager.is_active = True
            game_manager.starter_id = u_id
            await update.message.reply_text("🔥🔥 <b>يا شعب مونوبولي العظيم</b> 🔥🔥\n\nبدأت الروليت! اكتب <b>'انا'</b> للاشتراك", parse_mode='HTML')

    # 2. تسجيل الأعضاء (انا)
    elif text == "انا" and game_manager.is_active:
        game_manager.add_player(u_id, u_name)
        # نكتفي بالتسجيل الصامت في الذاكرة لضمان السرعة القصوى (بدون رد فردي)

    # 3. أمر النهاية (تم)
    elif text == "تم" and game_manager.is_active:
        if can_stop_roulette(u_id, game_manager.starter_id):
            await game_manager.run_elimination(update, context)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    print("البوت يعمل الآن بنجاح...")
    app.run_polling()
