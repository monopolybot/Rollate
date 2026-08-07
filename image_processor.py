# image_processor.py
import os
import shutil

# التحقق من توفر أداة tesseract في النظام لتجنب أي انهيار
TESSERACT_AVAILABLE = shutil.which("tesseract") is not None

if TESSERACT_AVAILABLE:
    import pytesseract
    from PIL import Image

async def process_user_album_image(image_path: str):
    """
    معالجة صورة الألبوم بأمان تام مع التحقق من توفر النظام
    """
    try:
        if not os.path.exists(image_path):
            return {"status": "error", "message": "Image not found"}

        if not TESSERACT_AVAILABLE:
            print("CRITICAL ERROR: tesseract is not installed on this server container.")
            return {"status": "error", "message": "Tesseract OCR is missing on server"}

        img = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(img, lang='ara+eng')
        
        cards = []
        words = extracted_text.split()
        for word in words:
            if len(word) > 3:
                cards.append({"card": word})

        return {"status": "success", "cards": cards}

    except Exception as e:
        print(f"CRITICAL ERROR in image_processor: {str(e)}")
        return {"status": "error", "message": str(e)}
