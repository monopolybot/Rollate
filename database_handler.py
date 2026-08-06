# database_handler.py
# نظام إدارة وتخزين البطاقات في قاعدة بيانات محلية خفيفة

import json
import os

DB_FILE = "trading_db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {"users": {}}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def update_user_cards(user_id, username, new_cards):
    """
    تحديث بطاقات العضو (يمكن تعديل المنطق لاحقاً لتمييز الزائد والناقص بدقة)
    """
    db = load_db()
    str_user_id = str(user_id)
    
    if str_user_id not in db["users"]:
        db["users"][str_user_id] = {
            "username": username,
            "cards": []
        }
    
    db["users"][str_user_id]["username"] = username
    db["users"][str_user_id]["cards"] = new_cards
    save_db(db)

def find_matches():
    """
    الابحث عن مطابقات بين الأعضاء (من يحتاج ما يملكه غيره)
    """
    db = load_db()
    users = db.get("users", {})
    matches = []
    
    # خوارزمية مبدئية للمطابقة بين الأعضاء المسجلين
    user_ids = list(users.keys())
    for i in range(len(user_ids)):
        for j in range(i + 1, len(user_ids)):
            u1 = users[user_ids[i]]
            u2 = users[user_ids[j]]
            
            # البحث عن تقاطع في البطاقات بين العضوين
            common_cards = [c for c in u1["cards"] if c in u2["cards"]]
            if common_cards:
                matches.append({
                    "user1": u1["username"],
                    "user2": u2["username"],
                    "cards": common_cards
                })
    return matches
