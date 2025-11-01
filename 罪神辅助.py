import tkinter as tk
from tkinter import messagebox
import ctypes
import sys
import keyboard
import psutil
import threading
import time

class GTAKillerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("罪神辅助(快捷键杀进程)")
        self.root.geometry("300x180")
        self.root.resizable(False, False)
        
        # 目标进程名称
        self.target_process = "GTA5_Enhanced.exe"
        
        # 检查并获取管理员权限
        if not self.is_admin():
            self.run_as_admin()
            sys.exit(0)
        
        # 创建界面元素
        self.label = tk.Label(
            root, 
            text=f"按End键结束GTA进程", 
            font=("SimHei", 12)
        )
        self.label.pack(expand=True)
        
        self.status_label = tk.Label(
            root, 
            text="等待操作...", 
            font=("SimHei", 10),
            fg="gray"
        )
        self.status_label.pack(pady=10)
        
        # 进程检测状态标签
        self.detection_label = tk.Label(
            root, 
            text="进程检测中...", 
            font=("SimHei", 10),
            fg="blue"
        )
        self.detection_label.pack(pady=5)
        
        # 注册热键
        keyboard.add_hotkey('end', self.kill_gta_process)
        
        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # 标记进程是否已提示过
        self.process_detected = False
        
        # 启动进程检测线程
        self.detection_running = True
        self.detection_thread = threading.Thread(target=self.detect_process, daemon=True)
        self.detection_thread.start()
    
    def is_admin(self):
        """检查程序是否以管理员权限运行"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def run_as_admin(self):
        """以管理员权限重新运行程序（不显示命令行窗口）"""
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 0
        )
    
    def kill_gta_process(self):
        """结束目标进程"""
        killed = False
        
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if proc.info['name'] == self.target_process:
                    proc.kill()
                    killed = True
                    self.status_label.config(text=f"已结束进程: {self.target_process}", fg="green")
                    # 重置检测标记，以便下次进程启动时再次提示
                    self.process_detected = False
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        if not killed:
            self.status_label.config(text=f"未找到进程: {self.target_process}", fg="red")
    
    def detect_process(self):
        """检测目标进程是否启动"""
        while self.detection_running:
            process_running = False
            
            # 检查进程是否在运行
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] == self.target_process:
                        process_running = True
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            # 更新检测状态
            if process_running:
                self.detection_label.config(text=f"进程正在运行: {self.target_process}", fg="orange")
                # 如果是新检测到的进程，显示提示
                if not self.process_detected:
                    self.process_detected = True
                    # 在主线程中显示消息框
                    self.root.after(0, self.show_process_detected_message)
            else:
                self.detection_label.config(text=f"进程未运行: {self.target_process}", fg="gray")
            
            # 每2秒检测一次
            time.sleep(1)
    
    def show_process_detected_message(self):
        """显示进程检测到的提示消息"""
        messagebox.showinfo(
            "进程检测", 
            f"检测到 {self.target_process} 进程已启动！\n按End键可以结束该进程。"
        )
    
    def on_close(self):
        """窗口关闭时的清理操作"""
        self.detection_running = False
        self.detection_thread.join(timeout=1.0)
        keyboard.unhook_all_hotkeys()
        self.root.destroy()

if __name__ == "__main__":
    # 确保中文显示正常
    root = tk.Tk()
    app = GTAKillerApp(root)
    root.mainloop()