r""" 
# python pdf2imgs.py "C:\Users\pc\OneDrive\图书馆\Zotero\storage\7P9VBRXD\Bubeck 等 - 2023 - Sparks of Artificial General Intelligence Early e.pdf" ""
"""

import os
import sys
import time
import shutil
from pdf2image import convert_from_path, convert_from_bytes # python -m pip install pdf2image
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from PIL import Image


pdf_path = sys.argv[1] # 绝对路径
# 得到绝对路径
pdf_path = os.path.abspath(pdf_path)
print("pdf_path: ", pdf_path)
pdf_name = pdf_path.split("\\")[-1].split(".pdf")[0] # 获取pdf文件名

"""
pdf_name = pdf_path.split("\\")[-1].split(".")[0] # 获取pdf文件名
print("pdf_name: ", pdf_name)
# 创建 pdfs 文件夹，如果存在就忽略
pdfs_dir = "pdfs"
os.makedirs(pdfs_dir, exist_ok=True)
# 在 pdfs 文件夹中创建 pdf_name 文件夹，如果存在就忽略
pdfs_pdf_name_dir = os.path.join("pdfs", pdf_name)
os.makedirs(pdfs_pdf_name_dir, exist_ok=True)

# 把 pdf_path 文件复制到 pdfs 文件夹中，并等待复制完成
# 获取源文件的文件名
pdf_filename = os.path.basename(pdf_path)
print("源文件名(pdf_filename)：", pdf_filename)
pdfs_folder = pdfs_pdf_name_dir
# 构建目标文件的完整路径
destination_path = os.path.join(pdfs_folder, pdf_filename)
print("目标文件路径(destination_path)：", destination_path)
# 文件复制标志
file_copied = False
while not file_copied:
    try:
        # 复制文件到目标文件夹
        shutil.copy2(pdf_path, destination_path)
        # 确认文件已成功复制
        if os.path.exists(destination_path):
            print("文件复制成功")
            file_copied = True
        else:
            print("文件复制失败，等待后重试")
            time.sleep(1)  # 等待 5 秒后重试复制
    except Exception as e:
        print("发生错误：", e)
        print("等待后重试")
        time.sleep(1)  # 等待 5 秒后重试复制
"""


# 创建 pdfs_pdf_name_imgs_dir 文件夹，如果存在就忽略
# pdfs_pdf_name_imgs_dir = os.path.join(pdfs_pdf_name_dir, "imgs")
# 如果 sys.argv[2] 不为空，就用 sys.argv[2] 作为 pdfs_pdf_name_imgs_dir
if len(sys.argv) == 3:
    pdfs_pdf_name_imgs_dir = sys.argv[2] # 绝对路径
os.makedirs(pdfs_pdf_name_imgs_dir, exist_ok=True)
# # 创建 pdfs_pdf_name_imgs_zh_dir 文件夹，如果存在就忽略
# pdfs_pdf_name_imgs_zh_dir = os.path.join(pdfs_pdf_name_dir, "imgs_zh")
# os.makedirs(pdfs_pdf_name_imgs_zh_dir, exist_ok=True)



# 获取pdf_path文件所在目录
pdf_dir = os.path.dirname(pdf_path)
# imgs_dir = pdf_dir
temp_dir = "pdfs"
imgs_dir = os.path.join(temp_dir, pdf_name)
os.makedirs(imgs_dir, exist_ok=True)
print("imgs_dir: ", imgs_dir)
imgs_dir = pdfs_pdf_name_imgs_dir #
imgs_path = os.path.join(imgs_dir, pdf_name + ".png")
print("imgs_path: ", imgs_path)
# images_from_path = convert_from_path(pdf_path, output_folder=imgs_dir, output_file=pdf_name, fmt='jpg', poppler_path = "poppler-23.01.0\\Library\\bin")
# print(images_from_path)
images_from_path = convert_from_path(pdf_path, poppler_path = "poppler-23.01.0\\Library\\bin")
# images_from_path = convert_from_path(pdf_path, poppler_path = "poppler-23.01.0\\Library\\bin", dpi=300)
# print(images_from_path)
imgs = []
for i, page in enumerate(images_from_path):
#   img_path = os.path.join(imgs_dir, f"{pdf_name}_page_{i+1}.png")
  img_path = os.path.join(imgs_dir, f"{i+1}.png")
  print("img_path: ", img_path)
  page.save(img_path) # 1.png, 2.png, 3.png
  # print(type(page)) # <class 'PIL.JpegImagePlugin.JpegImageFile'>
  #
#   imgs.append(page) # 拼接成一个长图
# sizes = [img.size for img in imgs]
# joint = Image.new('RGB', (sizes[0][0], sum([size[1] for size in sizes])))
# loc = 0
# for img, size in zip(imgs, sizes):
#   joint.paste(img, (0, loc))
#   loc += size[1]
# joint.save(imgs_path)

# 运行
# python .\pdf2imgs.py test.pdf
# python .\pdf2imgs.py "C:\Users\dcsco\OneDrive\图书馆\Zotero\storage\7P9VBRXD\Bubeck 等 - 2023 - Sparks of Artificial General Intelligence Early e.pdf"