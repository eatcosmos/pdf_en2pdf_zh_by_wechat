""" 
运行方法
python imgs2pdf.py 'C:\\Users\\dcsco\\OneDrive\\Filesystem\\tools\\tool_pdf_translator\\pdfs\\Bubeck 等 - 2023 - Sparks of Artificial General Intelligence Early e\\imgs_zh'
"""

import os
from PIL import Image
import sys

def imgs_to_pdf(img_folder):
  # image_files = [f for f in os.listdir(img_folder) if f.endswith('.png')]
  extensions = ('.png', '.jpg', '.jpeg')
  image_files = [f for f in os.listdir(img_folder) if f.lower().endswith(extensions)]
  # image_files.sort(key=lambda x: int(x.split('_')[2].split('.')[0]))
  image_files.sort(key=lambda x: int(x.split('.')[0]))
  images = [Image.open(os.path.join(img_folder, img_file)) for img_file in image_files]
  
  # Bubeck 等 - 2023 - Sparks of Artificial General Intelligence Early e_page_1.png
  # pdf_path = image_files[0] = image_files[0].split('_page_1')[0] + '_zh.pdf'
  pdf_path = sys.argv[2]
  print(f"pdf_path: {pdf_path}")
  # pdf_path = os.path.join(img_folder, 'test_zh.pdf')
  # 如果sys.argv[2]存在，就用它作为输出文件名
  if len(sys.argv) == 3:
    pdf_path = sys.argv[2]
  print(f"pdf_path: {pdf_path}")
  print(len(images))
  images[0].save(pdf_path, save_all=True, append_images=images[1:], format='PDF', quality=100)

if __name__ == "__main__":
  if len(sys.argv) == 3:
    img_folder = sys.argv[1]
    imgs_to_pdf(img_folder)
  else:
    print("Usage: python imgs2pdf.py img_folder_path")

# 运行
# python imgs2pdf.py temp/test/
#
