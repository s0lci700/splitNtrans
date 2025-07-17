import os
from split import split_pages
from extract import filename_to_int, ocr_image, translate_text, embed_text_on_image

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Split images, OCR, translate, and embed text.")
    parser.add_argument("input_folder", help="Folder with original scanned images (PNG)")
    parser.add_argument("-s", "--split_output", default="output", help="Output folder for split pages")
    parser.add_argument("-e", "--extract_output", default="extracted_texts", help="Folder to save OCR and translation results")
    args = parser.parse_args()

    # Step 1: Split images
    print("Splitting images...")
    split_pages(args.input_folder, args.split_output)

    # Step 2: OCR, translate, and embed text
    print("Processing split images...")
    os.makedirs(args.extract_output, exist_ok=True)
    for filename in sorted(os.listdir(args.split_output), key=filename_to_int):
        if filename.lower().endswith(".png"):
            path = os.path.join(args.split_output, filename)
            text = ocr_image(path)
            translated = translate_text(text)

            # Save text file
            output_txt_path = os.path.join(args.extract_output, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_txt_path, "w", encoding="utf-8") as f:
                f.write("=== ORIGINAL TEXT ===\n")
                f.write(text + "\n\n")
                f.write("=== TRANSLATION ===\n")
                f.write(translated + "\n")

            # Embed translated text on image and save
            output_img_path = os.path.join(args.extract_output, f"{os.path.splitext(filename)[0]}_translated.png")
            embed_text_on_image(path, translated, output_img_path, position=(10, 10), font_size=24)

            print(f"Processed {filename} → {output_txt_path}, {output_img_path}")
