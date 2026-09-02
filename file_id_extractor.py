
# file_id_extractor.py
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

async def extract_file_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return
        
    file_id = None
    file_type = ""
    
    if msg.voice:
        file_id = msg.voice.file_id
        file_type = "بصمة صوتية (Voice)"
    elif msg.audio:
        file_id = msg.audio.file_id
        file_type = "ملف صوتي (Audio)"
    elif msg.video:
        file_id = msg.video.file_id
        file_type = "فيديو (Video)"
    elif msg.video_note:
        file_id = msg.video_note.file_id
        file_type = "فيديو دائري (Video Note)"
    elif msg.photo:
        file_id = msg.photo[-1].file_id
        file_type = "صورة (Photo)"
        
    if file_id:
        await msg.reply_text(
            f"**تم استخراج المعرّف بنجاح للـ {file_type}:**\n`{file_id}`",
            parse_mode="Markdown"
        )

# دالة لتسجيل الهاندلر في الملف الرئيسي (تعمل حصرياً في الخاص)
def register_extractor_handler(application):
    private_media_filter = filters.ChatType.PRIVATE & (
        filters.VOICE | filters.AUDIO | filters.VIDEO | filters.VIDEO_NOTE | filters.PHOTO
    )
    application.add_handler(MessageHandler(private_media_filter, extract_file_id_handler))
  
