# database_handler.py
# نظام إدارة وتخزين البطاقات مع حفظ الـ ID الحقيقي لمنشن صحيح 100%

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
    تحديث بطاقات العضو وحفظ الـ user_id الحقيقي لضمان صحة المنشن
    """
    db = load_db()
    str_user_id = str(user_id)
    
    if str_user_id not in db["users"]:
        db["users"][str_user_id] = {
            "user_id": user_id,
            "username": username,
            "cards": {}
        }
    
    db["users"][str_user_id]["username"] = username
    db["users"][str_user_id]["user_id"] = user_id
    
    for item in new_cards:
        card_name = item.get("card")
        status = item.get("status") # 'need' أو 'have'
        album = item.get("album")
        if card_name and status:
            db["users"][str_user_id]["cards"][card_name] = {
                "status": status,
                "album": album
            }
            
    save_db(db)

def find_matches():
    """
    البحث عن مطابقات صحيحة مع تمرير الـ ID الحقيقي واسم المستخدم للطرفين
    """
    db = load_db()
    users = db.get("users", {})
    matches = []
    
    user_ids = list(users.keys())
    for i in range(len(user_ids)):
        for j in range(i + 1, len(user_ids)):
            u1 = users[user_ids[i]]
            u2 = users[user_ids[j]]
            
            u1_cards = u1.get("cards", {})
            u2_cards = u2.get("cards", {})
            
            common_cards = []
            
            # 1. هل U1 يملك الكرت (زائد) و U2 يطلبه (ناقص)؟
            for card, info in u1_cards.items():
                if info.get("status") == "have" and card in u2_cards and u2_cards[card].get("status") == "need":
                    common_cards.append({
                        "card": card, 
                        "giver_name": u1["username"],
                        "giver_id": u1["user_id"],
                        "receiver_name": u2["username"],
                        "receiver_id": u2["user_id"]
                    })
            
            # 2. هل U2 يملك الكرت (زائد) و U1 يطلبه (ناقص)؟
            for card, info in u2_cards.items():
                if info.get("status") == "have" and card in u1_cards and u1_cards[card].get("status") == "need":
                    common_cards.append({
                        "card": card, 
                        "giver_name": u2["username"],
                        "giver_id": u2["user_id"],
                        "receiver_name": u1["username"],
                        "receiver_id": u1["user_id"]
                    })
            
            if common_cards:
                matches.append({
                    "cards": common_cards
                })
                
    return matches
