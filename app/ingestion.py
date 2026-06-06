import fitz
from PIL import Image
from app.ocr import extract_text_from_image

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text()

        if not text.strip():
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = extract_text_from_image(img)

        pages.append({"page": i, "text": text})

    return pages