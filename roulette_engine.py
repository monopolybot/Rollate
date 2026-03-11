import random
import asyncio
from telegram import Update
from telegram.constants import ParseMode
from database import add_win, reset_user_wins
from config import POINTS_TO_WIN

class RouletteGame:
    def __init__(self):
        self.is_active = False
        self.starter_id = None
        self.players = {} # {user_id: name}

    def add_player(self, user_id, name):
        self.players[user_id] = name

    async def run_elimination(self, update: Update, context):
        if not self.players:
            await update.message.reply_text("❌ لم يسجل أحد في الروليت بعد!")
            return

        all_players = list(self.players.items())
        # خلط الأسماء لضمان العشوائية المطلقة
        random.shuffle(all_players)
        
        # اختيار الفائز
        winner_id, winner_name = random.choice(all_players)
        # اختيار المستبعدين (بحد أقصى 8 للعرض بشكل أنيق)
        others = [p for p in all_players if p[0] != winner_id]
        excluded_list = others[:8]

        header = "<b>-> قائمة المشاركين بالروليت:</b>\n\n"
        sent_msg = await update.message.reply_text(header, parse_mode=ParseMode.HTML)

        current_display = header
        # محاكاة تأثير الاستبعاد التدريجي لبوت TON
        for i, (p_id, p_name) in enumerate(excluded_list, 1):
            emoji = random.choice(["👓", "👀", "👤", "🧤"])
            current_display += f"{i} <b>مستبعد:</b> <a href='tg://user?id={p_id}'>{p_name}</a> {emoji}\n"
            
            # تحديث الرسالة كل اسمين لسرعة الأداء وتجنب الحظر
            if i % 2 == 0:
                await sent_msg.edit_text(current_display, parse_mode=ParseMode.HTML)
                await asyncio.sleep(0.7)

        # النتيجة النهائية للجولة
        current_wins = add_win(winner_id, winner_name)
        
        final_footer = f"\n<b>- الفائز بالروليت: ( <a href='tg://user?id={winner_id}'>{winner_name}</a> ) 🥳🎉</b>"
        final_footer += f"\n📊 <b>رصيد النقاط الحالي: {current_wins}/{POINTS_TO_WIN}</b>"

        # إذا وصل للنقطة الخامسة (التتويج الملكي)
        if current_wins >= POINTS_TO_WIN:
            final_footer = (
                f"\n\n👑 <b>لوحة التتويج الملكي</b> 👑\n"
                f"━━━━━━━━━━━━━━\n"
                f"✨ <b>البطل:</b> <a href='tg://user?id={winner_id}'>{winner_name}</a>\n"
                f"✅ <b>أتمّ 5 انتصارات ساحقة!</b>\n"
                f"━━━━━━━━━━━━━━\n"
                f"<b>مبارك اللقب الأسطوري! 🎊🔥</b>"
            )
            reset_user_wins(winner_id)

        await sent_msg.edit_text(current_display + final_footer, parse_mode=ParseMode.HTML)
        
        # تصفير الجولة
        self.is_active = False
        self.players = {}

game_manager = RouletteGame()
