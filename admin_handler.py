from telegram import Update
from config import OWNER_ID, ALLOWED_GROUPS

async def is_user_admin(update: Update, context):
    """التحقق مما إذا كان المستخدم مشرفاً في المجموعة"""
    if update.effective_user.id == OWNER_ID:
        return True
    
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # جلب قائمة المشرفين وتخزينها مؤقتاً لسرعة الأداء
    admins = await context.bot.get_chat_administrators(chat_id)
    admin_ids = [admin.user.id for admin in admins]
    
    return user_id in admin_ids

def can_stop_roulette(user_id, starter_id):
    """المشرف الذي بدأ الروليت أو المالك فقط يمكنهما الإنهاء"""
    return user_id == OWNER_ID or user_id == starter_id
