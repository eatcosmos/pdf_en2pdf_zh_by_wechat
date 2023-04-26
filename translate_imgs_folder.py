""" 
调用方法
python translate_imgs_folder.py "pdfs\Bubeck 等 - 2023 - Sparks of Artificial General Intelligence Early e\imgs" "pdfs\Bubeck 等 - 2023 - Sparks of Artificial General Intelligence Early e\imgs_zh"
"""
import re
import os
import sys
import time
import subprocess


# 定义输入和输出文件夹
imgs_folder = "imgs/"
imgs_zh_folder = "imgs_zh/"
# sys.argv[1]和sys.argv[2]分别是输入和输出文件夹，必须存在这两个参数，否则报错
if len(sys.argv) == 3: 
    imgs_folder = sys.argv[1]
    imgs_zh_folder = sys.argv[2]
    # 转换为绝对路径
    imgs_folder = os.path.abspath(imgs_folder)
    imgs_zh_folder = os.path.abspath(imgs_zh_folder)
else:
    sys.exit("请指定输入和输出文件夹")

# 确保输出文件夹存在
if not os.path.exists(imgs_zh_folder):
    os.makedirs(imgs_zh_folder)
# 获取输入文件夹中的所有文件
input_files = sorted(os.listdir(imgs_folder))
# 提取页码的正则表达式
page_number_regex = re.compile(r"_page_(\d+)\.png")

# 按照页码排序
def extract_page_number(file_name):
    match = page_number_regex.search(file_name)
    return int(match.group(1)) if match else 0

input_files.sort(key=extract_page_number)

loop_count = 1
i = 0
while i < len(input_files):
    input_file = input_files[i]
    i += 1
    print(f"正在处理 {input_file} ...")
    input_file_path = os.path.join(imgs_folder, input_file)
    # output_file_path = os.path.join(imgs_zh_folder, input_file.split("_page_")[1].replace(".png", ".jpg"))
    output_file_path = os.path.join(imgs_zh_folder, input_file.replace(".png", ".jpg"))
    print("\ninput_file_path: ", input_file_path)
    print("\noutput_file_path: ", output_file_path)

    # 跳过非图片文件
    if not input_file.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue
    # 如果 output_file_path 存在，跳过
    if os.path.exists(output_file_path): 
        continue
    
    # 调用 wechat_translate_a_img.py 脚本
    command = f'python wechat_translate_a_img.py \"{input_file_path}\" \"{output_file_path}\"'
    # process = subprocess.Popen(command, shell=True)
    os.system(command)

    # 等待输出文件存在
    elapsed_time = 0
    while not os.path.exists(output_file_path):
        print("等待输出文件存在...")
        wait_time = 3
        time.sleep(wait_time)  # 每隔0.1秒检查一次
        elapsed_time += 1
        if elapsed_time > 20 / wait_time:
            print("等待时间超过10秒，重新处理该文件")
            # process.terminate()
            break
    if elapsed_time > 3:
        i -= 1
        continue
    # if i == len(input_files):
    #     i = 0
    #     loop_count += 1
    # if loop_count > 2:
    #     break
        

    # # 检查输出文件是否存在
    # if os.path.exists(output_file_path):
    #     print(f"{input_file} 转换成功")
    #     process.terminate()  # 确保子进程已经结束
    # else:
    #     print(f"{input_file} 转换失败")
