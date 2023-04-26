""" 
调用方法
python wechat_translate_a_img.py test_page_16.png test_page_16_zh.jpg
"""

# 获取聊天输入框的位置，便于鼠标自动点击
# 获取 name 是 "输入" 的窗口
import os
import sys
import time
import psutil
import keyboard
import win32con
import pyautogui
import pyperclip
import pywinauto
import clipboard
import subprocess
import pytesseract
import win32process
import win32clipboard
from io import BytesIO
from PIL import ImageGrab
from pywinauto.application import Application
from pywinauto import Application, findwindows
#
import win32gui
win32gui.SW_RESTORE = win32con.SW_RESTORE

total_start_time = time.time()
start_time = time.time()
# 激活Wetchat.exe进程到前台
def find_pid_by_exe_name(exe_name):
    for process in psutil.process_iter(['pid', 'exe']):
        if process.info['exe'] and exe_name.lower() in process.info['exe'].lower():
            return process.info['pid']
    return None
# 调用函数
exe_name = 'WeChat.exe'
pid = find_pid_by_exe_name(exe_name)
app = Application(backend='uia').connect(process=pid)
print(app)
end_time = time.time()
time_elapsed = end_time - start_time
print("\n获取app...耗时: {:.2f} 秒\n".format(time_elapsed))


"""
# 获取主窗口
main_window = app.top_window()
# 将窗口设置为活动窗口
main_window.set_focus()
# 模拟按下 Win + 上箭头 键以最大化窗口
keyboard.press('win')
keyboard.press('up')
keyboard.release('up')
keyboard.release('win')
# time.sleep(5) # 若需要，等待一段时间
# 恢复窗口大小
# keyboard.press('win')
# keyboard.press('down')
# keyboard.release('down')
# keyboard.release('win')
"""

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
start_time = time.time()
top_windows = []
win32gui.EnumWindows(windowEnumerationHandler, top_windows)
for hwnd, window_title in top_windows:
    if "微信" == window_title:
        window_class = win32gui.GetClassName(hwnd)
        if "WeChatMainWndForPC" == window_class:
            # print("WeChatMainWndForPC: "+str(hwnd))
            # print("窗口句柄：", hwnd) # 263110
            # print("窗口标题：", window_title) # 微信
            # print("窗口类名：", window_class) # WeChatMainWndForPC
            win32gui.ShowWindow(hwnd,5)
            win32gui.ShowWindow(hwnd, win32gui.SW_RESTORE) # 还原窗口
            win32gui.SetForegroundWindow(hwnd)
            break
end_time = time.time()
time_elapsed = end_time - start_time
print("\n还原窗口...耗时: {:.2f} 秒\n".format(time_elapsed))

# 定义图片路径
image_path = "test_page_16.png"
# 如果没有传入图片路径，则使用默认图片
if len(sys.argv) < 2:
    print("未传入图片路径，使用默认图片")
else:
    image_path = sys.argv[1]
# 转为绝对路径
image_path = os.path.abspath(image_path)
# 输出图片路径是输入图片绝对路径 改为 _zh.jpg，输入图片的格式不确定
# 判断sys.argv[2]是否存在，如果存在，就用sys.argv[2]，否则就用默认值

# img_path = os.path.join(imgs_dir, f"{pdf_name}_page_{i+1}.png")

# image_zh_path = sys.argv[2] if len(sys.argv) > 2 else image_path.split(".")[0] + "_zh.jpg"
image_zh_path = sys.argv[2]
image_zh_path = os.path.abspath(image_zh_path) # 获取绝对路径
print("\n输入图片路径：{s}".format(s=image_path))
print("输出图片路径：{s}\n".format(s=image_zh_path))


start_time = time.time()
# 连接到微信应用
app = pywinauto.Application(backend="uia").connect(path="WeChat.exe")
wechat_window = app.top_window()
end_time = time.time()
time_elapsed = end_time - start_time
print("\n获取wechat_window...耗时: {:.2f} 秒\n".format(time_elapsed))

# utils.py
def close_window_if_exists(app, class_name):
    """如果存在指定类名的窗口，则关闭它"""

    # 检查指定类名的窗口是否存在
    if app.window(class_name=class_name).exists():
        # 如果存在，定位窗口
        target_window = app.window(class_name=class_name)
        print(f"{class_name} 窗口:", target_window)
        # 关闭窗口
        target_window.close()
    else:
        print(f"{class_name} 窗口不存在")
start_time = time.time()
# 例如，关闭名为 "ImagePreviewWnd" 的窗口：
# close_window_if_exists(app, "ImagePreviewWnd") # 2.00 秒
end_time = time.time()
time_elapsed = end_time - start_time
print("\n关闭名为 ImagePreviewWnd 的窗口...耗时: {:.2f} 秒\n".format(time_elapsed))


def wait_for_control(window, title, control_type):
    # 检查控件是否存在
    while not window.child_window(title=title, control_type=control_type).exists():
        # 如果不存在，则等待1秒钟，然后继续检查
        time.sleep(1)
    # 当控件出现时，获取它并返回
    control = window.child_window(title=title, control_type=control_type)
    return control
# 使用示例
# app = Application(backend="uia").connect(title_re=".*微信.*")
# wechat_window = app.window(title_re=".*微信.*")

# input_box = wait_for_control(wechat_window, "输入", "Edit")
import ctypes
# 初始化控件
input_box = None
retry_count = 3
start_time = time.time() # 统计耗时
while retry_count > 0:
    try:
        input_box = wechat_window.child_window(title="输入", control_type="Edit")
        break
    except Exception as e:
        print("COM 错误:", e)
        time.sleep(1)
        retry_count -= 1
        # break
    except Exception as e:
        print("其他错误:", e)
        break
input_box_rect = input_box.rectangle()
# print("输入框的矩形区域：", input_box_rect) # 输入框的矩形区域： (L381, T795, R1920, B960)
end_time = time.time()
time_elapsed = end_time - start_time
print("\n获取输入框的矩形区域...耗时: {:.2f} 秒\n".format(time_elapsed))

end_time = time.time()
time_elapsed = end_time - total_start_time
print("\n1...耗时: {:.2f} 秒\n".format(time_elapsed))

start_time = time.time()
input_box.set_focus() # 将焦点设置到输入框
input_box.type_keys('^a{BACKSPACE}') # 清空输入框

total_end_time = time.time()
time_elapsed = total_end_time - total_start_time
print("\n完成清空输入框...耗时: {:.2f} 秒\n".format(time_elapsed))

# 将图片复制到剪贴板
with open(image_path, "rb") as image_file:
    image = ImageGrab.Image.open(image_file)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_DIB, data)
    win32clipboard.CloseClipboard()
# 粘贴图片到输入框
input_box.type_keys('^v')
# time.sleep(1)
end_time = time.time()
time_elapsed = end_time - start_time
print("\n复制图片...耗时: {:.2f} 秒\n".format(time_elapsed))


"""
能获取 # 获取输入框控件
input_box = wechat_window.child_window(title="输入", control_type="Edit")
输入框控件右上角的位置吗，然后获取右上角位置往右往下移动20像素的位置，作为图片位置
"""


# 计算输入框右上角的位置
# 输入框的矩形区域： (L2290, T726, R2896, B858)
left_top_x = input_box_rect.left
left_top_y = input_box_rect.top
# 计算右上角位置往右往下移动20像素的位置
new_x = left_top_x + 50
new_y = left_top_y + 20

# 将焦点设置到输入框
# input_box.set_focus()
pyautogui.moveTo(new_x, new_y)
pyautogui.doubleClick() # 双击鼠标，很快就会弹出一个名为“图片查看”的窗口
# 等待“图片查看”窗口出现
# time.sleep(1)
"""
很好，完成了任务。图片复制到输入框了，此时鼠标在图片右下角边缘闪烁，需要鼠标移动到图片上，然后双击鼠标，会弹出一个Name是“图片查看”的窗口（class="ImagePreviewWnd"），然后需要鼠标定位到这个窗口上Name是“翻译”的控件，点击鼠标进行翻译
"""

start_time = time.time()
# 定位“图片查看”窗口
image_preview_window = app.window(class_name="ImagePreviewWnd")
end_time = time.time()
time_elapsed = end_time - start_time
print("获取image_preview_window...耗时: {:.2f} 秒".format(time_elapsed))

start_time = time.time()
# image_preview_window_rect = image_preview_window.rectangle()
# 获取“翻译”控件
translate_button = image_preview_window.child_window(title="翻译", control_type="Button") # 0.00 秒
# download_button = image_preview_window.child_window(title="另存为...", control_type="Button")
translate_button.click_input()
end_time = time.time()
time_elapsed = end_time - start_time
print("获取 translate_button...耗时: {:.2f} 秒".format(time_elapsed))
"""
start_time = time.time()
# 获取“翻译”控件的矩形区域
translate_button_rect = translate_button.rectangle() #  2.08 秒
end_time = time.time()
time_elapsed = end_time - start_time
print("获取 翻译 控件的矩形区域...耗时: {:.2f} 秒".format(time_elapsed))

start_time = time.time()
# 计算“翻译”控件的中心点位置
center_x = (translate_button_rect.left + translate_button_rect.right) // 2
center_y = (translate_button_rect.top + translate_button_rect.bottom) // 2
end_time = time.time()
time_elapsed = end_time - start_time
print("计算 翻译 控件的中心点位置...耗时: {:.2f} 秒".format(time_elapsed))

# 移动鼠标到“翻译”控件的中心点并单击
pyautogui.moveTo(center_x, center_y)
pyautogui.click()
"""

# 等待翻译结果出现
time.sleep(6) 
def is_translation_in_progress(window):
    # 获取窗口的矩形区域
    window_rect = window.rectangle()
    # 将 window_rect 转换为四元组
    bbox = (window_rect.left, window_rect.top, window_rect.right, window_rect.bottom)
    # 截取窗口图像
    screenshot = ImageGrab.grab(bbox)
    # 使用 pytesseract 识别文本
    text = pytesseract.image_to_string(screenshot, lang='chi_sim')
    fanyizhong = "翻译中" in text
    print("翻译中..." if fanyizhong else "翻译完成")
    return fanyizhong
# 等待翻译完成
# while is_translation_in_progress(image_preview_window):
#     time.sleep(1)  # 每隔1秒检查一次



end_time = time.time()
time_elapsed = end_time - total_start_time
print("\n2...耗时: {:.2f} 秒\n".format(time_elapsed))

""" 
很好，完成了任务。在Name是“图片查看”的窗口（class="ImagePreviewWnd"）上
然后需要鼠标定位到这个窗口上Name是“下载”的控件，然后移动鼠标到控件点击鼠标，会弹出一个Name是“另存为...”的窗口
模拟按下ctrl+v，会把剪贴板的字符串image_zh_path复制过去，然后点击保存按钮，保存按钮信息如下
How found:	Mouse move (1669,910)
	hwnd=0x003B0A20 32bit class="Button" style=0x50030001 ex=0x4
ChildId:	0
Interfaces:	IEnumVARIANT IOleWindow IAccIdentity
Impl:	Local oleacc proxy
AnnotationID:	01000080200A3B00FCFFFFFF00000000
Name:	"保存(S)"
Value:	[null]
Role:	按下按钮 (0x2B)
"""

import pywinauto
from pywinauto import clipboard
import pyautogui
import time

# 将需要粘贴的字符串存储在剪贴板中
# image_zh_path = "C:\\Users\\dcsco\\OneDrive\\Filesystem\\tools\\tool_pdf_translator\\test_page_16_zh.jpg"
print(f"image_zh_path: {image_zh_path}")
# 检查文件是否存在
if os.path.exists(image_zh_path):
    try:
        # 删除文件
        os.remove(image_zh_path)
        print(f"文件 {image_zh_path} 已被成功删除")
    except Exception as e:
        print(f"删除文件时发生错误: {e}")
else:
    print(f"文件 {image_zh_path} 不存在")
# clipboard.copy(image_zh_path)
pyperclip.copy(image_zh_path)

# 定位“图片查看”窗口
image_preview_window = app.window(class_name="ImagePreviewWnd")

# 定位并点击“另存为...”按钮
download_button = image_preview_window.child_window(title="另存为...", control_type="Button")
download_button.click_input()
time.sleep(0.5)

# 等待“另存为...”窗口出现
# time.sleep(2)

# 定位“另存为...”窗口
# save_as_window = app.window(title="另存为...")
# save_as_dialog = app.window(class_name="#32770", hwnd=0x007F0632)
# save_as_dialog = app.window(title="另存为...", class_name="#32770")
# wechat_process_id = app.process
# save_as_dialog = app.window(title="另存为...", class_name="#32770", process=wechat_process_id)



# 模拟按下 Ctrl+V 将文件名粘贴到文件名输入框
pyautogui.hotkey("ctrl", "v")
# time.sleep(0.5) # 等待文件名粘贴完成
# sys.exit(0)
# 模拟按下回车键
pyautogui.press("enter")
time.sleep(0.5)
# # 模拟按下tab键
# pyautogui.press("tab")
# # 模拟按下回车键
# pyautogui.press("enter")
# time.sleep(0.5) # 等待文件保存完成

""" 
你可以将查找和点击 "是(Y)" 按钮的操作封装为一个函数，如下所示：
"""
from pywinauto import timings
def click_yes_button():
    try:
        # 等待 "确认另存为" 窗口出现
        confirm_save_as_window = app.window(title="确认另存为")
        timings.WaitUntilPasses(2, 0.5, confirm_save_as_window.exists)
        # 定位 "是(Y)" 按钮
        yes_button = confirm_save_as_window.child_window(title="是(Y)", control_type="Button")
        # 点击 "是(Y)" 按钮
        yes_button.click()
    except:
        print("确认另存为 窗口未找到")
# 调用函数
# click_yes_button()

# 定位并点击“保存”按钮
# save_button = save_as_dialog.child_window(title="保存(S)", control_type="Button")
# save_button.click_input()

start_time = time.time()
# 例如，关闭名为 "ImagePreviewWnd" 的窗口：
# close_window_if_exists(app, "ImagePreviewWnd") # 2.00 秒
# app.window(class_name="ImagePreviewWnd").close()
# 模拟安装 ESC 键关闭窗口
pyautogui.press("esc")
end_time = time.time()
time_elapsed = end_time - start_time
print("关闭名为 ImagePreviewWnd 的窗口...耗时: {:.2f} 秒".format(time_elapsed))

total_end_time = time.time()
time_elapsed = total_end_time - total_start_time
print("\nwechat_translate_a_img.py...耗时: {:.2f} 秒\n".format(time_elapsed))