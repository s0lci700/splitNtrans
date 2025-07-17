import os
from PIL import Image
import pytesseract
# from deep_translator import GoogleTranslator
from deep_translator import GoogleTranslator
# from googletrans import Translator

# Configure tesseract path if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def filename_to_int(filename):
    # Extract the numeric part before the first underscore for sorting
    base = filename.split('_')[0]
    try:
        return int(base)
    except ValueError:
        return float('inf')  # Non-numeric filenames go last


def ocr_image(image_path):
    image = Image.open(image_path)
    # Optional: Convert to grayscale, increase contrast, etc.
    image = image.convert('L')
    # OCR - Russian
    text = pytesseract.image_to_string(image, lang='rus')
    return text

def translate_text(text, lang_from='ru', lang_to='en'):
    try:
        translated = GoogleTranslator(source=lang_from, target=lang_to).translate(text)
    except Exception as e:
        translated = f"[Translation error: {e}]"
    return translated

def embed_text_on_image(image_path, text, output_path, position=(10, 10), font_size=24):
    from PIL import ImageDraw, ImageFont
    image = Image.open(image_path).convert('RGB')
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    draw.text(position, text, fill=(255, 0, 0), font=font)
    image.save(output_path)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OCR and translate Russian text from image")
    parser.add_argument("image_folder", help="Folder with images to OCR")
    parser.add_argument("-o", "--output", default="extracted_texts", help="Folder to save the results")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    for filename in sorted(os.listdir(args.image_folder), key=filename_to_int):
        if filename.lower().endswith(".png"):
            path = os.path.join(args.image_folder, filename)
            text = ocr_image(path)
            translated = translate_text(text)

            # Save text file
            output_txt_path = os.path.join(args.output, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_txt_path, "w", encoding="utf-8") as f:
                f.write("=== ORIGINAL TEXT ===\n")
                f.write(text + "\n\n")
                f.write("=== TRANSLATION ===\n")
                f.write(translated + "\n")

            # Embed translated text on image and save
            output_img_path = os.path.join(args.output, f"{os.path.splitext(filename)[0]}_translated.png")
            embed_text_on_image(path, translated, output_img_path, position=(10, 10), font_size=24)

            print(f"Processed {filename} → {output_txt_path}, {output_img_path}")
