from tinydb import TinyDB, Query
import os

# المسار المخصص للـ Volume في Northflank لضمان عدم ضياع البيانات
db_path = '/app/data/roulette_db.json'

# التأكد من وجود المجلد لتجنب الأخطاء
os.makedirs(os.path.dirname(db_path), exist_ok=True)

db = TinyDB(db_path)
User = Query()

def get_user_wins(user_id):
    user = db.get(User.id == user_id)
    return user.get('wins', 0) if user else 0

def add_win(user_id, name):
    user = db.get(User.id == user_id)
    if user:
        new_wins = user.get('wins', 0) + 1
        db.update({'wins': new_wins, 'name': name}, User.id == user_id)
        return new_wins
    else:
        db.insert({'id': user_id, 'name': name, 'wins': 1})
        return 1

def reset_user_wins(user_id):
    db.update({'wins': 0}, User.id == user_id)

# الدالة الجديدة لتصفير نقاط جميع اللاعبين عند انتهاء الموسم أو فوز ملك الروليت
def reset_all_players_wins():
    db.update({'wins': 0})
