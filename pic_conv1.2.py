from concurrent.futures import ProcessPoolExecutor
import os
from PIL import Image
import pillow_avif
import glob

def process_image(img_path):
    try:
        output_base_dir_path = '/Users/kanae/OneDrive/画像/VRChat/Converted/'
        basename_img = os.path.splitext(os.path.basename(img_path))[0]
        year, month = os.path.basename(os.path.dirname(img_path)).split('-')
        output_dir_path = os.path.join(output_base_dir_path, f'{year}-{month}')

        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path, exist_ok=True)

        avif_name = os.path.join(output_dir_path, f"{basename_img}_av.avif")

        # 既に存在する場合はスキップ
        if os.path.exists(avif_name):
            return f"Skipped (already exists): {avif_name}"

        img = Image.open(img_path)
        width, height = img.size
        new_width, new_height = (1920, int(1920 * (9 / 16))) if width > height else (int(1920 * (9 / 16)), 1920)
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        resized_img.save(avif_name, format="AVIF")
        return f"Converted and saved: {avif_name}"
    except Exception as e:
        return f"Error processing {img_path}: {e}"

def main():
    base_dir_path = '/Users/kanae/OneDrive/画像/VRChat/'
    img_paths = []
    for year in range(2020, 2031):
        for month in range(1, 13):
            dir_path = os.path.join(base_dir_path, f'{year}-{month:02d}')
            if os.path.exists(dir_path):
                img_paths.extend(glob.glob(os.path.join(dir_path, '*.png')))

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_image, img_paths))

    for result in results:
        print(result)

if __name__ == '__main__':
    main()
