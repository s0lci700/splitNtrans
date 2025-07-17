# splitNtrans
script made to split the pages of a scan, then extract and translate the text
# SplitNTrans

This project provides a workflow for processing scanned book images:
1. **Splitting** double-page scans into separate single-page images.
2. **Extracting text** from each page using OCR (Tesseract).
3. **Translating** the extracted text from Russian to English.
4. **Embedding** the translated text onto the corresponding image.

## Features
- Batch process PNG images from a folder.
- Output split images, extracted text files, and images with embedded translations.
- Modular code: easy to extend or adapt for other languages or formats.

## Requirements
- Python 3.8+
- Tesseract OCR (install from https://github.com/tesseract-ocr/tesseract)
- Python packages: `pillow`, `pytesseract`, `deep-translator`

Install dependencies:
```sh
pip install pillow pytesseract deep-translator
```

## Usage

### 1. Prepare your folders
- Place your scanned PNG images in a folder (e.g., `input_files/`).

### 2. Run the main script
```sh
python main.py input_files -s output -e extracted_texts
```
- `input_files`: Folder with original scanned images (PNG)
- `-s output`: Output folder for split pages (default: `output`)
- `-e extracted_texts`: Output folder for OCR and translation results (default: `extracted_texts`)

### 3. Output
- Split images: `output/`
- Text and translation files: `extracted_texts/*.txt`
- Images with embedded translation: `extracted_texts/*_translated.png`

## Customization
- Change OCR language or translation target in `extract.py`.
- Adjust text embedding position and font size in `embed_text_on_image()`.

## Troubleshooting
- Make sure Tesseract is installed and its path is set in `extract.py`.
- If you get font errors, ensure `arial.ttf` is available or use a different font.

## License
MIT
