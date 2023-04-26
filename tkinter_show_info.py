import sys
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter.font import Font

class WarningDialog:
    def __init__(self, parent, message):
        self.top = tk.Toplevel(parent)
        self.top.title('提示')

        font = Font(size=16, weight='bold')
        self.label = tk.Label(self.top, text=message, font=font)
        self.label.pack(pady=10)

        # 计算标签的文本宽度和高度，并根据宽度和高度设置窗口的大小
        req_width = self.label.winfo_reqwidth() + 20
        req_height = self.label.winfo_reqheight() + 50
        self.top.geometry('{}x{}'.format(req_width, req_height))

        # 计算对话框应该显示的位置，并设置对话框的位置
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        dialog_width = self.top.winfo_reqwidth()
        dialog_height = self.top.winfo_reqheight()
        x = int((screen_width - dialog_width) / 2)
        y = int((screen_height - dialog_height) / 2)
        self.top.geometry('+{}+{}'.format(x, y))

        # 让对话框的窗口中心和屏幕中心重合
        self.top.update_idletasks()
        window_width = self.top.winfo_width()
        window_height = self.top.winfo_height()
        x = (screen_width - window_width) // 2
        # x = 0
        y = (screen_height - window_height) // 2
        y = 0
        self.top.geometry('+{}+{}'.format(x, y))

        self.top.protocol("WM_DELETE_WINDOW", self.close) # 绑定窗口关闭事件
        self.top.after(3000, self.close)  # 3 秒钟后自动关闭窗口

    def close(self):
        self.top.destroy()
        self.top.quit()  # 退出应用程序

root = tk.Tk()
root.withdraw()

message = '请登录微信，并打开任意对话的输入框...'
# 如果在命令行中指定了消息，则使用命令行中的消息
if len(sys.argv) > 1:
  message = sys.argv[1]
dialog = WarningDialog(root, message)

root.mainloop()
