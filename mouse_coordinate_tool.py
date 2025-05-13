import tkinter as tk
from tkinter import ttk, messagebox
import time
import win32gui
import win32api
import win32con
import os
from PIL import ImageGrab, ImageTk
import numpy as np

class MouseCoordinateTool:
    def __init__(self, root):
        self.root = root
        self.root.title("鼠标坐标测量工具")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # 创建保存截图的文件夹
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        
        # 初始化变量
        self.ldplayer_handle = None
        self.ldplayer_rect = None
        self.screenshot = None
        self.photo = None
        self.coordinates = []
        self.is_recording = False
        self.last_mouse_pos = (0, 0)
        self.last_relative_pos = (0, 0)
        
        # 创建界面元素
        self.create_widgets()
        
        # 查找雷电模拟器窗口
        self.find_ldplayer_window()
        
        # 开始更新鼠标位置
        self.update_mouse_position()
    
    def create_widgets(self):
        # 创建样式
        style = ttk.Style()
        style.configure("TButton", font=("微软雅黑", 10))
        style.configure("TLabel", font=("微软雅黑", 10))
        style.configure("TEntry", font=("微软雅黑", 10))
        
        # 创建标题
        title_label = ttk.Label(self.root, text="凯旋棋牌坐标测量工具", font=("微软雅黑", 14, "bold"))
        title_label.pack(pady=10)
        
        # 创建窗口信息区域
        window_frame = ttk.LabelFrame(self.root, text="窗口信息", padding=10)
        window_frame.pack(fill="x", padx=20, pady=5)
        
        # 窗口句柄
        handle_frame = ttk.Frame(window_frame)
        handle_frame.pack(fill="x", pady=5)
        ttk.Label(handle_frame, text="雷电模拟器句柄:").pack(side="left", padx=5)
        self.handle_label = ttk.Label(handle_frame, text="未找到")
        self.handle_label.pack(side="left", padx=5)
        
        # 窗口位置
        pos_frame = ttk.Frame(window_frame)
        pos_frame.pack(fill="x", pady=5)
        ttk.Label(pos_frame, text="窗口位置:").pack(side="left", padx=5)
        self.pos_label = ttk.Label(pos_frame, text="未找到")
        self.pos_label.pack(side="left", padx=5)
        
        # 创建按钮区域
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=20, pady=5)
        
        # 查找窗口按钮
        find_btn = ttk.Button(button_frame, text="查找雷电模拟器", command=self.find_ldplayer_window)
        find_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # 截图按钮
        screenshot_btn = ttk.Button(button_frame, text="截取窗口", command=self.take_screenshot)
        screenshot_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # 开始/停止记录按钮
        self.record_btn = ttk.Button(button_frame, text="开始记录坐标", command=self.toggle_recording)
        self.record_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # 清除坐标按钮
        clear_btn = ttk.Button(button_frame, text="清除坐标", command=self.clear_coordinates)
        clear_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # 保存坐标按钮
        save_btn = ttk.Button(button_frame, text="保存坐标", command=self.save_coordinates)
        save_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # 创建鼠标位置显示区域
        mouse_frame = ttk.LabelFrame(self.root, text="鼠标位置", padding=10)
        mouse_frame.pack(fill="x", padx=20, pady=5)
        
        # 屏幕坐标
        screen_frame = ttk.Frame(mouse_frame)
        screen_frame.pack(fill="x", pady=5)
        ttk.Label(screen_frame, text="屏幕坐标:").pack(side="left", padx=5)
        self.screen_pos_label = ttk.Label(screen_frame, text="(0, 0)")
        self.screen_pos_label.pack(side="left", padx=5)
        
        # 窗口相对坐标
        relative_frame = ttk.Frame(mouse_frame)
        relative_frame.pack(fill="x", pady=5)
        ttk.Label(relative_frame, text="窗口相对坐标:").pack(side="left", padx=5)
        self.relative_pos_label = ttk.Label(relative_frame, text="(0, 0)")
        self.relative_pos_label.pack(side="left", padx=5)
        
        # 创建截图显示区域
        image_frame = ttk.LabelFrame(self.root, text="窗口截图", padding=10)
        image_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.image_label = ttk.Label(image_frame)
        self.image_label.pack(fill="both", expand=True)
        
        # 创建坐标列表区域
        coord_frame = ttk.LabelFrame(self.root, text="记录的坐标", padding=10)
        coord_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # 创建坐标列表
        self.coord_listbox = tk.Listbox(coord_frame, height=5, font=("微软雅黑", 9))
        self.coord_listbox.pack(fill="both", expand=True)
        
        # 创建状态栏
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", padx=20, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="就绪")
        self.status_label.pack(side="left")
    
    def find_ldplayer_window(self):
        """查找雷电模拟器窗口"""
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if "雷电模拟器" in title:
                    self.ldplayer_handle = hwnd
                    return False
            return True
        
        self.ldplayer_handle = None
        win32gui.EnumWindows(callback, None)
        
        if self.ldplayer_handle:
            self.handle_label.config(text=str(self.ldplayer_handle))
            self.update_window_rect()
            self.status_label.config(text="已找到雷电模拟器窗口")
        else:
            self.handle_label.config(text="未找到")
            self.pos_label.config(text="未找到")
            self.status_label.config(text="未找到雷电模拟器窗口")
    
    def update_window_rect(self):
        """更新窗口位置信息"""
        if self.ldplayer_handle:
            try:
                left, top, right, bottom = win32gui.GetWindowRect(self.ldplayer_handle)
                self.ldplayer_rect = (left, top, right, bottom)
                self.pos_label.config(text=f"({left}, {top}, {right}, {bottom})")
            except Exception as e:
                self.pos_label.config(text=f"获取失败: {str(e)}")
        else:
            self.pos_label.config(text="未找到")
    
    def take_screenshot(self):
        """截取雷电模拟器窗口"""
        if not self.ldplayer_handle:
            messagebox.showerror("错误", "未找到雷电模拟器窗口")
            return
        
        try:
            self.update_window_rect()
            left, top, right, bottom = self.ldplayer_rect
            
            # 截取窗口
            self.screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            
            # 调整大小以适应显示区域
            display_width = self.image_label.winfo_width()
            display_height = self.image_label.winfo_height()
            
            if display_width > 1 and display_height > 1:
                # 计算缩放比例
                width, height = self.screenshot.size
                scale = min(display_width / width, display_height / height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                
                # 缩放图像
                resized = self.screenshot.resize((new_width, new_height), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(resized)
                self.image_label.config(image=self.photo)
            
            # 保存截图
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f'screenshots/ldplayer_{timestamp}.png'
            self.screenshot.save(filename)
            
            self.status_label.config(text=f"截图已保存到: {filename}")
        except Exception as e:
            self.status_label.config(text=f"截图失败: {str(e)}")
            messagebox.showerror("错误", f"截图失败: {str(e)}")
    
    def update_mouse_position(self):
        """更新鼠标位置信息"""
        if self.ldplayer_handle and self.ldplayer_rect:
            try:
                # 获取鼠标屏幕坐标
                screen_x, screen_y = win32api.GetCursorPos()
                self.screen_pos_label.config(text=f"({screen_x}, {screen_y})")
                
                # 计算相对于窗口的坐标
                left, top, _, _ = self.ldplayer_rect
                relative_x = screen_x - left
                relative_y = screen_y - top
                self.relative_pos_label.config(text=f"({relative_x}, {relative_y})")
                
                # 如果正在记录，且鼠标位置发生变化，则记录坐标
                if self.is_recording and (screen_x, screen_y) != self.last_mouse_pos:
                    self.last_mouse_pos = (screen_x, screen_y)
                    self.last_relative_pos = (relative_x, relative_y)
                    
                    # 检查是否在窗口内
                    if (0 <= relative_x <= self.ldplayer_rect[2] - self.ldplayer_rect[0] and 
                        0 <= relative_y <= self.ldplayer_rect[3] - self.ldplayer_rect[1]):
                        # 记录坐标
                        self.coordinates.append((relative_x, relative_y))
                        self.coord_listbox.insert(tk.END, f"({relative_x}, {relative_y})")
                        self.coord_listbox.see(tk.END)
            except Exception as e:
                pass
        
        # 每秒更新10次
        self.root.after(100, self.update_mouse_position)
    
    def toggle_recording(self):
        """切换记录状态"""
        self.is_recording = not self.is_recording
        
        if self.is_recording:
            self.record_btn.config(text="停止记录坐标")
            self.status_label.config(text="正在记录坐标...")
        else:
            self.record_btn.config(text="开始记录坐标")
            self.status_label.config(text="已停止记录坐标")
    
    def clear_coordinates(self):
        """清除记录的坐标"""
        self.coordinates = []
        self.coord_listbox.delete(0, tk.END)
        self.status_label.config(text="已清除所有坐标")
    
    def save_coordinates(self):
        """保存记录的坐标"""
        if not self.coordinates:
            messagebox.showinfo("提示", "没有坐标可保存")
            return
        
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f'screenshots/coordinates_{timestamp}.txt'
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("# 凯旋棋牌坐标数据\n")
                f.write("# 格式: (x, y) - 相对于窗口左上角的坐标\n")
                f.write("# 时间: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
                
                for i, (x, y) in enumerate(self.coordinates):
                    f.write(f"坐标 {i+1}: ({x}, {y})\n")
            
            self.status_label.config(text=f"坐标已保存到: {filename}")
            messagebox.showinfo("成功", f"坐标已保存到: {filename}")
        except Exception as e:
            self.status_label.config(text=f"保存坐标失败: {str(e)}")
            messagebox.showerror("错误", f"保存坐标失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseCoordinateTool(root)
    root.mainloop() 