import tkinter as tk
from tkinter import messagebox
import ctypes
import sys
import keyboard
import psutil

class GTAKillerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("罪神辅助(快捷键杀进程)")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        
        # 检查并获取管理员权限
        if not self.is_admin():
            self.run_as_admin()
            sys.exit(0)
        
        # 创建界面元素
        self.label = tk.Label(
            root, 
            text="按End键结束GTA进程", 
            font=("SimHei", 12)
        )
        self.label.pack(expand=True)
        
        self.status_label = tk.Label(
            root, 
            text="等待操作...", 
            font=("SimHei", 10),
            fg="gray"
        )
        self.status_label.pack(pady=20)
        
        # 注册热键
        keyboard.add_hotkey('end', self.kill_gta_process)
        
        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def is_admin(self):
        """检查程序是否以管理员权限运行"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def run_as_admin(self):
        """以管理员权限重新运行程序（不显示命令行窗口）"""
        # 修改最后一个参数为 0（SW_HIDE），隐藏命令行窗口
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 0
        )
    
    def kill_gta_process(self):
        """结束GTA进程"""
        process_name = "GTA5_Enhanced.exe"
        killed = False
        
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if proc.info['name'] == process_name:
                    proc.kill()
                    killed = True
                    self.status_label.config(text=f"已结束进程: {process_name}", fg="green")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        if not killed:
            self.status_label.config(text=f"未找到进程: {process_name}", fg="red")
    
    def on_close(self):
        """窗口关闭时的清理操作"""
        keyboard.unhook_all_hotkeys()
        self.root.destroy()

if __name__ == "__main__":
    # 确保中文显示正常
    root = tk.Tk()
    app = GTAKillerApp(root)
    root.mainloop()