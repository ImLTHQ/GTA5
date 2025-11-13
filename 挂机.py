import sys
import ctypes
import random
import time
from pynput.keyboard import Controller

def is_admin():
    """判断当前进程是否拥有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """以管理员权限重新启动当前脚本"""
    # 获取当前脚本的路径
    script = sys.argv[0]
    # 使用ShellExecuteW请求管理员权限重启脚本
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, script, None, 1  # 1表示显示窗口
    )

def main():
    # 模拟按键的核心逻辑
    keyboard = Controller()
    keys = ['w', 'a', 's', 'd']
    
    print("自动挂机中...")

    while True:
        key = random.choice(keys)
        keyboard.press(key)
        time.sleep(1)  # 按住1秒
        keyboard.release(key)
        time.sleep(1)  # 等待1秒后继续

if __name__ == "__main__":
    # 检查权限，若不是管理员则提权
    if not is_admin():
        run_as_admin()
        # 提权后会启动新进程，因此退出当前非管理员进程
        sys.exit(0)
    # 若已获取管理员权限，则执行主逻辑
    main()