import tkinter as tk
from tkinter import scrolledtext
import pyautogui
import threading
import time
from datetime import datetime
import sys
import os
import ctypes
import random
import keyboard

# 设置 PyAutoGUI 的安全设置
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1

# Windows API 常量
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

class PreventSleepApp:
    def __init__(self, root):
        self.root = root
        self.root.title("防止睡眠工具")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # 设置最小窗口大小
        self.root.minsize(400, 300)
        
        # 创建控制区域（上方）
        control_frame = tk.Frame(root, pady=10)
        control_frame.pack(fill=tk.X)
        
        # 创建按钮
        self.start_button = tk.Button(
            control_frame, 
            text="不要睡觉", 
            command=self.start_monitoring,
            width=15,
            height=2
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(
            control_frame, 
            text="停止监听", 
            command=self.stop_monitoring,
            width=15,
            height=2,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        # 创建日志区域（下方）
        log_frame = tk.Frame(root)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # 创建日志文本框
        self.log_area = scrolledtext.ScrolledText(
            log_frame, 
            wrap=tk.WORD,
            height=15
        )
        self.log_area.pack(fill=tk.BOTH, expand=True)
        
        # 初始化监控线程相关变量
        self.monitoring_thread = None
        self.is_monitoring = False
        
        # 记录初始信息
        self.log_message("程序已启动，点击【不要睡觉】开始防止屏幕休眠")
        
        # 设置关闭窗口的处理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def prevent_system_sleep(self):
        """使用 Windows API 阻止系统休眠"""
        try:
            ctypes.windll.kernel32.SetThreadExecutionState(
                ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
            )
        except Exception as e:
            self.log_message(f"设置系统状态时出错: {str(e)}")

    def restore_system_sleep(self):
        """恢复系统休眠设置"""
        try:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        except Exception as e:
            self.log_message(f"恢复系统状态时出错: {str(e)}")

    def simulate_activity(self):
        """模拟用户活动"""
        try:
            # 随机选择一个动作
            action = random.choice([
                self.simulate_mouse_move,
                self.simulate_key_press,
                self.simulate_scroll,
                self.simulate_file_access
            ])
            action()
        except Exception as e:
            self.log_message(f"模拟活动时出错: {str(e)}")

    def simulate_mouse_move(self):
        """模拟鼠标移动"""
        current_x, current_y = pyautogui.position()
        offset_x = random.randint(-10, 10)
        offset_y = random.randint(-10, 10)
        pyautogui.moveRel(offset_x, offset_y, duration=0.1)
        pyautogui.moveRel(-offset_x, -offset_y, duration=0.1)
        self.log_message("已模拟鼠标移动")

    def simulate_key_press(self):
        """模拟按键"""
        # 模拟按下和释放Scroll Lock键，这个键一般不会影响正常使用
        keyboard.press_and_release('scroll lock')
        self.log_message("已模拟按键操作")

    def simulate_scroll(self):
        """模拟滚动操作"""
        pyautogui.scroll(1)
        time.sleep(0.1)
        pyautogui.scroll(-1)
        self.log_message("已模拟滚轮操作")

    def simulate_file_access(self):
        """模拟文件访问"""
        temp_file = "temp_activity.txt"
        try:
            # 写入当前时间戳
            with open(temp_file, "w") as f:
                f.write(str(datetime.now()))
            # 立即读取
            with open(temp_file, "r") as f:
                f.read()
            # 删除临时文件
            os.remove(temp_file)
            self.log_message("已模拟文件操作")
        except Exception as e:
            self.log_message(f"文件操作时出错: {str(e)}")

    def log_message(self, message):
        """向日志区域添加消息"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_text = f"[{current_time}] {message}\n"
        self.log_area.insert(tk.END, log_text)
        self.log_area.see(tk.END)

    def start_monitoring(self):
        """开始监控"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self.monitor_task)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            
            self.prevent_system_sleep()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.log_message("防止睡眠监控已启动")

    def stop_monitoring(self):
        """停止监控"""
        if self.is_monitoring:
            self.is_monitoring = False
            self.restore_system_sleep()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.log_message("防止睡眠监控已停止")

    def monitor_task(self):
        """监控任务的具体实现"""
        try:
            while self.is_monitoring:
                try:
                    # 执行随机活动模拟
                    self.simulate_activity()
                    
                    # 每30秒执行一次活动
                    for _ in range(30):
                        if not self.is_monitoring:
                            break
                        time.sleep(1)
                    
                except Exception as e:
                    self.log_message(f"执行活动时发生错误: {str(e)}")
                    time.sleep(5)  # 发生错误时等待5秒再继续
                    
        except Exception as e:
            self.log_message(f"监控任务发生错误: {str(e)}")
            self.stop_monitoring()

    def on_closing(self):
        """窗口关闭时的处理"""
        self.stop_monitoring()
        self.root.destroy()
        sys.exit()

def main():
    root = tk.Tk()
    app = PreventSleepApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 