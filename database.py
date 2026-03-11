from tinydb import TinyDB, Query

# إنشاء قاعدة بيانات سريعة وصغيرة
db = TinyDB('roulette_db.json')
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
