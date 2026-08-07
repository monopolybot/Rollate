# image_processor.py
# نظام معالجة الصور واستخراج البطاقات باستخدام pytesseract (خفيف جداً وبدون نماذج ضخمة)

import os
from PIL import Image
import pytesseract
from cards_engine import match_card_text

async def process_user_album_image(image_path):
    try:
        # فتح الصورة باستخدام Pillow
        img = Image.open(image_path)
        
        # استخراج النصوص باللغتين العربية والإنجليزية عبر Tesseract
        # (ملاحظة: ara+eng تدعم النص العربي والإنكليزي معاً)
        extracted_text = pytesseract.image_to_string(img, lang='ara+eng')
        
        # مطابقة النصوص مع البطاقات الـ 21
        matched_cards = match_card_text(extracted_text)
        
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
        # تنظيف الصورة المؤقتة بعد الانتهاء
        if os.path.exists(image_path):
            os.remove(image_path)
