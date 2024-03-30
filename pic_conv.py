#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import pillow_avif
import os
import glob

# 元の画像があるディレクトリ
dir_path = '/Users/kanae/OneDrive/画像/VRChat/2023-10/'
# 保存先のディレクトリパスを指定
output_dir_path = '/Users/kanae/OneDrive/画像/VRChat/Converted/2023-10/'

# 保存先のディレクトリが存在しない場合は作成
if not os.path.exists(output_dir_path):
    os.makedirs(output_dir_path)

file_list = glob.glob(os.path.join(dir_path, '*.png'))

for img_path in file_list:
	img = Image.open(img_path)
	basename_img = os.path.splitext(os.path.basename(img_path))[0]

	avif_name = os.path.join(output_dir_path, f"{basename_img}_av.avif")

	width, height = img.size
	if width / height > 1:  # 横長の画像
		new_width = 1920
		new_height = int(new_width * (9 / 16))
	else:  # 縦長の画像
		new_height = 1920
		new_width = int(new_height * (9 / 16))

	resized_img = img.resize((new_width, new_height), resample=Image.LANCZOS)
	resized_img.save(avif_name, format="AVIF")

	print(f"Converted and saved: {avif_name}")