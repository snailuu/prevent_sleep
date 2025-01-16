import tkinter as tk
from tkinter import scrolledtext
import pyautogui
import threading
import time
from datetime import datetime
import sys

# 设置 PyAutoGUI 的安全设置
pyautogui.FAILSAFE = False  # 禁用 fail-safe
pyautogui.PAUSE = 0.1  # 设置操作间隔时间

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
    
    def log_message(self, message):
        """向日志区域添加消息"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_text = f"[{current_time}] {message}\n"
        self.log_area.insert(tk.END, log_text)
        self.log_area.see(tk.END)  # 自动滚动到最新内容
    
    def start_monitoring(self):
        """开始监控"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self.monitor_task)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.log_message("防止睡眠监控已启动")
    
    def stop_monitoring(self):
        """停止监控"""
        if self.is_monitoring:
            self.is_monitoring = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.log_message("防止睡眠监控已停止")
    
    def monitor_task(self):
        """监控任务的具体实现"""
        try:
            while self.is_monitoring:
                try:
                    # 获取当前鼠标位置
                    current_x, current_y = pyautogui.position()
                    
                    # 检查鼠标是否在屏幕边缘
                    screen_width, screen_height = pyautogui.size()
                    if (current_x <= 5 or current_x >= screen_width - 5 or 
                        current_y <= 5 or current_y >= screen_height - 5):
                        self.log_message("鼠标在屏幕边缘，跳过本次移动")
                        continue
                    
                    # 移动鼠标（在原位置附近小幅度移动）
                    pyautogui.moveRel(5, 0, duration=0.1)  # 向右移动5像素
                    pyautogui.moveRel(-5, 0, duration=0.1)  # 移回原位
                    
                    self.log_message("鼠标移动完成，等待下一次移动...")
                    
                except pyautogui.FailSafeException:
                    self.log_message("检测到鼠标在屏幕角落，跳过本次移动")
                except Exception as e:
                    self.log_message(f"鼠标移动时发生错误: {str(e)}")
                
                # 等待1分钟
                for _ in range(60):
                    if not self.is_monitoring:
                        break
                    time.sleep(1)
                    
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