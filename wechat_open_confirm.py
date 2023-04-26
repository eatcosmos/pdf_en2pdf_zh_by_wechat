import subprocess

# 调用 wechat_open.py 脚本
process = subprocess.Popen(['python', 'wechat_open.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate() # 等待进程执行完成，并获取标准输出和标准错误输出
returncode = process.wait() # 等待进程执行完成，并获取返回值
print(returncode) # 输出进程的返回值 0

# 再次调用 wechat_open.py 
process = subprocess.Popen(['python', 'wechat_open.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

