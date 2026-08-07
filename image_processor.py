# image_processor.py
# نظام معالجة الصور واستخراج البطاقات تلقائياً باستخدام OCR مع تثبيت مسار النماذج

import os
import easyocr
from cards_engine import match_card_text

# تحديد مجلد ثابت لتخزين نماذج الذكاء الاصطناعي لمنع إعادة تنزيلها مع كل ريستارت
MODEL_DIR = os.path.join(os.path.expanduser("~"), ".EasyOCR")

# تهيئة القارئ مع توجيهه للمسار الثابت للغة العربية والانجليزية
reader = easyocr.Reader(['ar', 'en'], model_storage_directory=MODEL_DIR, download_enabled=True)

async def process_user_album_image(image_path):
    try:
        # قراءة النص من الصورة
        results = reader.readtext(image_path, detail=0)
        full_extracted_text = " ".join(results)
        
        # مطابقة النصوص مع البطاقات الـ 21
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
        # تنظيف الصورة المؤقتها بعد الانتهاء
        if os.path.exists(image_path):
            os.remove(image_path)
