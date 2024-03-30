#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from concurrent.futures import ProcessPoolExecutor, as_completed
import os
from PIL import Image
import pillow_avif
import glob
from tqdm import tqdm
import time

def process_image(img_path, output_base_dir_path):
    avif_name = "Undefined"  # 初期値としてUndefinedを設定
    try:
        basename_img = os.path.splitext(os.path.basename(img_path))[0]
        year, month = os.path.basename(os.path.dirname(img_path)).split('-')
        output_dir_path = os.path.join(output_base_dir_path, f'{year}-{month}')

        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path, exist_ok=True)

        avif_name = os.path.join(output_dir_path, f"{basename_img}_av.avif")  # ここでavif_nameを定義

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
        # エラー発生時にもavif_nameが参照可能
        return f"Error processing {img_path} (Destination: {avif_name}): {e}"

def main():
    base_dir_path = '/Users/name/OneDrive/画像/VRChat/' #ここを自分のVRChatディレクトリ名に変えてください。
    output_base_dir_path = '/Users/name/OneDrive/画像/VRChat/Converted/' #ここを変換後の画像を保存したいディレクトリ名に変えてください。
    years = range(2020, 2031)
    months = range(1, 13)
    max_workers = os.cpu_count() // 2 if os.cpu_count() else 2

    for year in years:
        for month in months:
            dir_path = os.path.join(base_dir_path, f'{year}-{month:02d}')
            if os.path.exists(dir_path):
                img_paths = glob.glob(os.path.join(dir_path, '*.png'))
                with ProcessPoolExecutor(max_workers=max_workers) as executor, tqdm(total=len(img_paths), desc=f"Processing {year}-{month:02d}") as pbar:
                    futures = {executor.submit(process_image, img_path, output_base_dir_path): img_path for img_path in img_paths}
                    for future in as_completed(futures):
                        result = future.result()
                        tqdm.write(result)  # ここでtqdm.write()を使用
                        pbar.update(1)  # プログレスバーを更新

if __name__ == '__main__':
    main()