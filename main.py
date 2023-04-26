
r"""
调用方法
python main.py "Bringing the Web up to Speed with WebAssembly.pdf"

"""

import os
import sys
import time
import subprocess

total_start_time = time.time()
pdf_en_path = sys.argv[1].replace("\\", "\\\\")
# or use the alternative method
# pdf_path = os.path.normpath(sys.argv[1])
# 转换为绝对路径
pdf_en_path = os.path.abspath(pdf_en_path)
print(f"pdf_en_path: {pdf_en_path}")
pdf_zh_path = pdf_en_path.replace(".pdf", "_zh.pdf")
print(f"pdf_zh_path: {pdf_zh_path}")

# 获取pdf页数
import PyPDF2
def get_pdf_page_count(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        return len(pdf_reader.pages)
# pdf_en_path = "/path/to/pdf_en.pdf"
pdf_en_page_count = get_pdf_page_count(pdf_en_path)
print(f"Number of pages in the PDF: {pdf_en_page_count}")

# pdfs_dir = "pdfs"
# pdfs_dir = "~\Desktop\pdfs" # 保存到桌面pdfs/
# 获取桌面路径 
desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
pdfs_dir = os.path.join(desktop_path, "pdfs")
pdf_name = pdf_en_path.split("\\")[-1].split(".pdf")[0] # 获取pdf文件名
print(f"pdf_name: {pdf_name}")
pdfs_pdf_name_dir = os.path.join(pdfs_dir, pdf_name)
pdfs_pdf_name_imgs_folder = os.path.join(pdfs_pdf_name_dir, "imgs")
pdfs_pdf_name_imgs_zh_folder = os.path.join(pdfs_pdf_name_dir, "imgs_zh")
print(f"pdfs_pdf_name_dir: {pdfs_pdf_name_dir}")
print(f"pdfs_pdf_name_imgs_folder: {pdfs_pdf_name_imgs_folder}")
print(f"pdfs_pdf_name_imgs_zh_folder: {pdfs_pdf_name_imgs_zh_folder}")

# sys.exit(0)
def run_command(command):
    result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print("Command executed successfully")
        print("Output:", result.stdout)
        return result.stdout
    else:
        print("Command execution failed")
        print("Error:", result.stderr)
        sys.exit(1)

# 启动微信
command = f"python wechat_open.py"
print(f"启动微信: {command}")
run_command(command)
# 验证启动
command = f"python wechat_open_confirm.py"
print(f"验证启动: {command}")
run_command(command)

# pdf_en2imgs
# python pdf2imgs.py "C:\Users\pc\OneDrive\图书馆\Zotero\storage\7P9VBRXD\Bubeck 等 - 2023 - Sparks of Artificial General Intelligence Early e.pdf"
command = f"python pdf2imgs.py \"{pdf_en_path}\" \"{pdfs_pdf_name_imgs_folder}\""
print(f"pdf_en2imgs: {command}")
# run_command(command)
os.system(command)
# 等待 pdfs_pdf_name_imgs_folder 里面文件达到 pdf_en_page_count 个
while True: 
    imgs_count = len(os.listdir(pdfs_pdf_name_imgs_folder))
    if imgs_count == pdf_en_page_count:
        print(f"imgs_count: {imgs_count}")
        break
    else:
        print(f"imgs_count: {imgs_count}")
        time.sleep(1)

# imgs2imgs_zh
# python translate_imgs_folder.py "pdfs\Bubeck 等 - 2023 - Sparks of Artificial General Intelligence Early e\imgs" "pdfs\Bubeck 等 - 2023 - Sparks of Artificial General Intelligence Early e\imgs_zh"
command = f"python translate_imgs_folder.py \"{pdfs_pdf_name_imgs_folder}\" \"{pdfs_pdf_name_imgs_zh_folder}\""
print(f"imgs2imgs_zh: {command}")
# run_command(command)
os.system(command)
# 等待 pdfs_pdf_name_imgs_folder 里面文件达到 pdf_en_page_count 个
while True: 
    imgs_count = len(os.listdir(pdfs_pdf_name_imgs_zh_folder))
    if imgs_count == pdf_en_page_count:
        print(f"imgs_zh_count: {imgs_count}")
        break
    else:
        print(f"imgs_zh_count: {imgs_count}")
        os.system(command)
        time.sleep(1)

# imgs_zh2pdf_zh
# python imgs2pdf.py 'C:\Users\dcsco\Desktop\pdfs\TaskMatrix.AI - Completing Tasks by Connecting Foundation Models with Millions_Liang_Wu_Song_Wu_Xia_Liu_Ou_Lu_Ji_Mao_Wang_Shou_Gong_Duan_2023\imgs_zh' 'C:\Users\dcsco\OneDrive\图书馆\附件\创业\out.pdf'
command = f"python imgs2pdf.py \"{pdfs_pdf_name_imgs_zh_folder}\" \"{pdf_zh_path}\""
print(f"imgs_zh2pdf_zh: {command}")
# run_command(command)
os.system(command)

total_end_time = time.time()
time_elapsed = total_end_time - total_start_time
print("\n总耗时: {:.2f} 秒\n".format(time_elapsed))

# 用默认pdf阅读器打开pdf_zh_path，并退出main.py
os.startfile(pdf_zh_path) # 用默认pdf阅读器打开pdf_zh_path 
# sys.exit(0) # 退出main.py 
 