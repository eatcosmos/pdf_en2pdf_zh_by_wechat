import time
import psutil
from pywinauto.application import Application
import ctypes
from pywinauto import Application, findwindows
import win32gui
import sys
import win32process
import win32con
import subprocess
win32gui.SW_RESTORE = win32con.SW_RESTORE

def weait_for_WeChatMainWndForPC():
    while True:
        find_WeChatMainWndForPC = False
        top_windows = []
        win32gui.EnumWindows(windowEnumerationHandler, top_windows)
        
        for hwnd, window_title in top_windows:
            if "微信" == window_title:
                window_class = win32gui.GetClassName(hwnd)
                # print("窗口句柄：", hwnd)
                # print("窗口标题：", window_title) 
                # print("窗口类名：", window_class) # WeChatMainWndForPC
                if "WeChatMainWndForPC" == window_class:
                    # print("WeChatMainWndForPC: "+str(hwnd))
                    print("窗口句柄：", hwnd)
                    print("窗口标题：", window_title) 
                    print("窗口类名：", window_class) # WeChatMainWndForPC
                    win32gui.ShowWindow(hwnd,5)
                    win32gui.ShowWindow(hwnd, win32gui.SW_RESTORE) # 还原窗口
                    win32gui.SetForegroundWindow(hwnd)
                    find_WeChatMainWndForPC = True
                    break
        if find_WeChatMainWndForPC:
            print("find_WeChatMainWndForPC: "+"True")
            break
        # print("请登录微信，并定位到发送信息的窗口...")
        message = '请登录微信，并定位到发送信息的窗口...'
        process = subprocess.Popen(['python', 'tkinter_show_info.py', message], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate() # 等待进程执行完成，并获取标准输出和标准错误输出
        returncode = process.wait() # 等待进程执行完成，并获取返回值
        # time.sleep(3)

def get_windows_by_pid(pid):
    windows = []
    def enum_windows_callback(hwnd, windows):
        window_pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        if window_pid == pid:
            windows.append(hwnd)
        return True
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def bring_window_to_front1(pid):
    app = Application().connect(process=pid)
    app_top_windows = app.windows()
    
    if not app_top_windows:
        print(f"No window found for process id {pid}")
        return
    
    main_window = app_top_windows[0]
    main_window.set_focus()

    SWP_NOMOVE = 0x0002
    SWP_NOSIZE = 0x0001

    ctypes.windll.user32.SetWindowPos(main_window.handle, -1, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)

def bring_window_to_front2(pid):
    try:
        app = Application().connect(process=pid)
        app_top_windows = app.windows()
        
        if not app_top_windows:
            print(f"No window found for process id {pid}")
            return

        main_window = app_top_windows[0]
        main_window.set_focus()

        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001

        ctypes.windll.user32.SetWindowPos(main_window.handle, -1, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
    except findwindows.ProcessNotFoundError:
        print(f"Process with id {pid} not found")
        
# 激活Wetchat.exe进程到前台
def find_pid_by_exe_name(exe_name):
    for process in psutil.process_iter(['pid', 'exe']):
        if process.info['exe'] and exe_name.lower() in process.info['exe'].lower():
            return process.info['pid']
    return None

exe_name = 'WeChat.exe'
pid = find_pid_by_exe_name(exe_name)
if pid:
    print(f'找到进程ID： {pid}')
    # bring_window_to_front2(pid)
    # 获取进程 ID 为 1234 的所有窗口句柄
    pid = pid
    # windows = get_windows_by_pid(pid)
    # print(windows)
    # sys.exit(0)
else:
    print(f'未找到 {exe_name} 对应的进程')
    # 常用方式二：启动微信进程 （注意路径中特殊字符的转义，/和\，不注意有时会出错）
    app = Application(backend="uia").start(r'C:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe') # 弹出登录
    print(app) # <pywinauto.application.Application object at 0x000001C6763A92E0>
    # 弹出登录界面
    weait_for_WeChatMainWndForPC()
    sys.exit(0)
    



# 常用方式一：连接已有微信进程（进程号在 任务管理器-详细信息 可以查看,项目中一般根据进程名称自动获取）
app = Application(backend='uia').connect(process=pid)

if 1:
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    
    for hwnd, window_title in top_windows:
        if "微信" == window_title:
            window_class = win32gui.GetClassName(hwnd)
            if "WeChatMainWndForPC" == window_class:
                # print("WeChatMainWndForPC: "+str(hwnd))
                print("窗口句柄：", hwnd)
                print("窗口标题：", window_title) 
                print("窗口类名：", window_class) # WeChatMainWndForPC
                win32gui.ShowWindow(hwnd,5)
                win32gui.ShowWindow(hwnd, win32gui.SW_RESTORE) # 还原窗口
                win32gui.SetForegroundWindow(hwnd)
                break
    if 0:
        i_list = []
        for i in top_windows:
            # print(i)
            if "微信" == i[1].lower():
                print(i)
                # (67620, '微信')
                # (132488, '微信')
                # (198046, '微信')
                # print(type(i)) # <class 'tuple'>
                i_num = i[0]
                # i_num = 11667036
                win32gui.ShowWindow(i_num,5)
                # win32gui.SetForegroundWindow(i_num)
                i_list.append(i)
                # break
                
        # 假设i是包含多个tuple的列表
        # 按照tuple的第一个元素从小到大排序
        i_sorted = sorted(i_list, key=lambda x: x[0])
        # 输出排序结果
        for i in i_sorted:
            # print(i)
            pass
        i_num = i_sorted[1][0]
        print("i_num:", i_num)
        # win32gui.ShowWindow(i_num,5)
        # win32gui.SetForegroundWindow(i_num)
        # sys.exit(0)