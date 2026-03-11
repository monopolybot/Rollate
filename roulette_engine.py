import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from database import add_win, reset_user_wins, get_user_wins
from config import POINTS_TO_WIN

class RouletteGame:
    def __init__(self):
        self.is_active = False
        self.starter_id = None
        self.players = {}  # نستخدم قاموس لمنع التكرار والحفاظ على السرعة {user_id: name}

    def add_player(self, user_id, name):
        # تسجيل سريع في الذاكرة
        self.players[user_id] = name

    async def run_elimination(self, update: Update, context):
        if not self.players:
            await update.message.reply_text("❌ لا يوجد مشاركين في الروليت!")
            return

        all_players = list(self.players.items())
        random.shuffle(all_players)
        
        # اختيار الفائز عشوائياً والباقي مستبعدين (مثل نظام TON)
        winner_id, winner_name = random.choice(all_players)
        # نختار عينة للعرض كـ "مستبعدين" لزيادة الإثارة
        others = [p for p in all_players if p[0] != winner_id]
        display_excluded = others[:8]  # عرض أول 8 مستبعدين فقط

        status_msg = "<b>🔄 بدأت عملية التصفية الملكية...</b>\n\n"
        sent_msg = await update.message.reply_text(status_msg, parse_mode=ParseMode.HTML)

        # تأثير الاستبعاد (الدراما)
        for i, (p_id, p_name) in enumerate(display_excluded):
            status_msg += f"{i+1} <b>مستبعد:</b> <a href='tg://user?id={p_id}'>{p_name}</a>\n"
            if i % 2 == 0: # تحديث الرسالة كل اسمين لتجنب الحظر
                await sent_msg.edit_text(status_msg, parse_mode=ParseMode.HTML)
                await asyncio.sleep(0.5)

        # معالجة الفوز والنقاط
        current_wins = add_win(winner_id, winner_name)
        
        final_text = status_msg + f"\n🏆 <b>الفائز بالجولة:</b> ( <a href='tg://user?id={winner_id}'>{winner_name}</a> )\n"
        final_text += f"✨ <b>عدد انتصاراته حتى الآن:</b> {current_wins}/{POINTS_TO_WIN}"
        
        # تحقق من التتويج الملكي (5 نقاط)
        if current_wins >= POINTS_TO_WIN:
            final_text += f"\n\n👑🎊 <b>تتويج ملك الروليت الأسطوري</b> 🎊👑\n"
            final_text += f"المقاتل <a href='tg://user?id={winner_id}'>{winner_name}</a> ختم الـ 5 نقاط!"
            reset_user_wins(winner_id)

        await sent_msg.edit_text(final_text, parse_mode=ParseMode.HTML)
        self.is_active = False
        self.players = {}

game_manager = RouletteGame()
