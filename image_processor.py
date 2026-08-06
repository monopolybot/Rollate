# image_processor.py
# نظام معالجة الصور واستخراج البطاقات تلقائياً باستخدام OCR

import os
import easyocr
from cards_engine import match_card_text

# تهيئة القارئ ليدعم اللغتين العربية والإنجليزية
# (سيتم تحميل النموذج تلقائياً عند أول تشغيل)
reader = easyocr.Reader(['ar', 'en'])

async def process_user_album_image(image_path):
    """
    استقبال مسار الصورة، قراءة النصوص فيها، 
    ومطابقتها مع قائمة الـ 21 مجموعة لتحديد البطاقات بدقة.
    """
    try:
        # قراءة النصوص من الصورة
        results = reader.readtext(image_path, detail=0)
        
        # دمج النصوص المستخرجة في نص واحد للبحث
        full_extracted_text = " ".join(results)
        
        # مطابقة النصوص مع البطاقات عبر محرك الألبومات
        matched_cards = match_card_text(full_extracted_text)
        
        return {
            "status": "success",
            "cards": matched_cards
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        # تنظيف وحذف الملف المؤقت بعد الانتهاء للحفاظ على مساحة السيرفر
        if os.path.exists(image_path):
            os.remove(image_path)
