import os
from PIL import Image

def filename_to_int(filename):
    # Extract the numeric part before the first dot for sorting
    base = filename.split('.')[0]
    try:
        return int(base)
    except ValueError:
        return float('inf')  # Non-numeric filenames go last

def split_pages(input_folder, output_folder):
    
    os.makedirs(output_folder, exist_ok=True)
    num = 1
    for filename in sorted(os.listdir(input_folder), key=filename_to_int):
        if filename.endswith('.png'):
            file_path = os.path.join(input_folder, filename)
            image = Image.open(file_path)
            width, height = image.size
            
            middle = width // 2

            left_page = image.crop((0, 0, middle, height))
            right_page = image.crop((middle, 0, width, height))
            
            

            left_page.save(os.path.join(output_folder, f'{num}_a.png'))
            right_page.save(os.path.join(output_folder, f'{num}_b.png'))
            num += 1

            print(f"Split {filename} -> {num - 1}_a.png, {num - 1}_b.png")
            
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Split scanned book images into two pages.")
    parser.add_argument("input_folder", help="Folder with original scanned images (PNG)")
    parser.add_argument("-o", "--output", default="output", help="Output folder for split pages")

    args = parser.parse_args()

    split_pages(args.input_folder, args.output)