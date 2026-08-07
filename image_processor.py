# image_processor.py
import os
import pytesseract
from PIL import Image

async def process_user_album_image(image_path: str):
    """
    معالجة صورة الألبوم واستخراج النصوص والبطاقات باستخدام pytesseract مع التقاط الأخطاء بدقة
    """
    try:
        # التأكد من وجود الصورة
        if not os.path.exists(image_path):
            print(f"Error: Image path not found -> {image_path}")
            return {"status": "error", "message": "Image not found"}

        # فتح الصورة باستخدام PIL
        img = Image.open(image_path)

        # استخراج النصوص باستخدام pytesseract (اللغتين العربية والإنجليزية)
        extracted_text = pytesseract.image_to_string(img, lang='ara+eng')
        
        print(f"Extracted Text successfully: {extracted_text[:100]}...") # طباعة عينة للتأكد

        # هنا يمكنك مطابقة النصوص المستخرجة مع قائمة البطاقات لديك
        # سنقوم بإرجاع النصوص المكتشفة مؤقتاً للتأكد من عمل النظام
        cards = []
        # مثال مبسط لاستخراج الكلمات كبطاقات
        words = extracted_text.split()
        for word in words:
            if len(word) > 3:  # تصفية الكلمات القصيرة
                cards.append({"card": word})

        return {"status": "success", "cards": cards}

    except Exception as e:
        # طباعة الخطأ الحقيقي بالتفصيل في السجلات لمعرفته فوراً
        print(f"CRITICAL ERROR in image_processor: {str(e)}")
        return {"status": "error", "message": str(e)}
