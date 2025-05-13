import tkinter as tk
from tkinter import ttk, messagebox
import time
from GameHelper import GameHelper

class MouseControlTester:
    def __init__(self, root):
        self.root = root
        self.root.title("鼠标控制测试工具")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # 初始化GameHelper
        self.helper = GameHelper()
        
        # 创建界面元素
        self.create_widgets()
        
        # 记录上一次点击的坐标
        self.last_click_pos = None
        
    def create_widgets(self):
        # 创建样式
        style = ttk.Style()
        style.configure("TButton", font=("微软雅黑", 10))
        style.configure("TLabel", font=("微软雅黑", 10))
        style.configure("TEntry", font=("微软雅黑", 10))
        
        # 创建标题
        title_label = ttk.Label(self.root, text="雷电模拟器鼠标控制测试", font=("微软雅黑", 14, "bold"))
        title_label.pack(pady=20)
        
        # 创建坐标输入框
        coord_frame = ttk.LabelFrame(self.root, text="坐标输入", padding=10)
        coord_frame.pack(fill="x", padx=20, pady=10)
        
        # X坐标
        x_frame = ttk.Frame(coord_frame)
        x_frame.pack(fill="x", pady=5)
        ttk.Label(x_frame, text="X坐标:").pack(side="left", padx=5)
        self.x_entry = ttk.Entry(x_frame, width=10)
        self.x_entry.pack(side="left", padx=5)
        self.x_entry.insert(0, "0")
        
        # Y坐标
        y_frame = ttk.Frame(coord_frame)
        y_frame.pack(fill="x", pady=5)
        ttk.Label(y_frame, text="Y坐标:").pack(side="left", padx=5)
        self.y_entry = ttk.Entry(y_frame, width=10)
        self.y_entry.pack(side="left", padx=5)
        self.y_entry.insert(0, "0")
        
        # 创建按钮
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        # 移动鼠标按钮
        move_btn = ttk.Button(button_frame, text="移动鼠标", command=self.move_mouse)
        move_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # 点击鼠标按钮
        click_btn = ttk.Button(button_frame, text="点击鼠标", command=self.click_mouse)
        click_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # 双击鼠标按钮
        double_click_btn = ttk.Button(button_frame, text="双击鼠标", command=self.double_click_mouse)
        double_click_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # 创建日志区域
        log_frame = ttk.LabelFrame(self.root, text="操作日志", padding=10)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.log_text = tk.Text(log_frame, height=10, width=40, font=("微软雅黑", 9))
        self.log_text.pack(fill="both", expand=True)
        self.log_text.config(state="disabled")
        
        # 创建状态栏
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = ttk.Label(status_frame, text="就绪")
        self.status_label.pack(side="left")
        
        # 添加窗口信息显示
        info_frame = ttk.LabelFrame(self.root, text="窗口信息", padding=10)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        # 显示窗口句柄
        handle_frame = ttk.Frame(info_frame)
        handle_frame.pack(fill="x", pady=5)
        ttk.Label(handle_frame, text="窗口句柄:").pack(side="left", padx=5)
        self.handle_label = ttk.Label(handle_frame, text=str(self.helper.Handle))
        self.handle_label.pack(side="left", padx=5)
        
        # 显示窗口位置
        pos_frame = ttk.Frame(info_frame)
        pos_frame.pack(fill="x", pady=5)
        ttk.Label(pos_frame, text="窗口位置:").pack(side="left", padx=5)
        self.pos_label = ttk.Label(pos_frame, text="")
        self.pos_label.pack(side="left", padx=5)
        
        # 更新窗口位置信息
        self.update_window_info()
        
    def update_window_info(self):
        """更新窗口信息"""
        try:
            left, top, right, bottom = self.helper.GetWindowRect()
            self.pos_label.config(text=f"({left}, {top}, {right}, {bottom})")
        except Exception as e:
            self.pos_label.config(text=f"获取失败: {str(e)}")
        
        # 每秒更新一次
        self.root.after(1000, self.update_window_info)
    
    def log(self, message):
        """添加日志"""
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
    
    def get_coordinates(self):
        """获取输入的坐标"""
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            return x, y
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字坐标")
            return None, None
    
    def move_mouse(self):
        """移动鼠标到指定坐标"""
        x, y = self.get_coordinates()
        if x is None or y is None:
            return
        
        try:
            self.status_label.config(text=f"正在移动鼠标到 ({x}, {y})...")
            self.root.update()
            
            # 调用GameHelper的LeftClick2函数，但不实际点击
            self.helper.LeftClick2((x, y), click=False)
            
            self.log(f"鼠标已移动到坐标 ({x}, {y})")
            self.status_label.config(text=f"鼠标已移动到 ({x}, {y})")
            self.last_click_pos = (x, y)
        except Exception as e:
            self.log(f"移动鼠标失败: {str(e)}")
            self.status_label.config(text="移动鼠标失败")
            messagebox.showerror("错误", f"移动鼠标失败: {str(e)}")
    
    def click_mouse(self):
        """点击鼠标"""
        x, y = self.get_coordinates()
        if x is None or y is None:
            return
        
        try:
            self.status_label.config(text=f"正在点击坐标 ({x}, {y})...")
            self.root.update()
            
            # 调用GameHelper的LeftClick2函数进行点击
            self.helper.LeftClick2((x, y))
            
            self.log(f"已在坐标 ({x}, {y}) 点击鼠标")
            self.status_label.config(text=f"已在 ({x}, {y}) 点击鼠标")
            self.last_click_pos = (x, y)
        except Exception as e:
            self.log(f"点击鼠标失败: {str(e)}")
            self.status_label.config(text="点击鼠标失败")
            messagebox.showerror("错误", f"点击鼠标失败: {str(e)}")
    
    def double_click_mouse(self):
        """双击鼠标"""
        x, y = self.get_coordinates()
        if x is None or y is None:
            return
        
        try:
            self.status_label.config(text=f"正在双击坐标 ({x}, {y})...")
            self.root.update()
            
            # 调用GameHelper的LeftClick2函数进行双击
            self.helper.LeftClick2((x, y), double=True)
            
            self.log(f"已在坐标 ({x}, {y}) 双击鼠标")
            self.status_label.config(text=f"已在 ({x}, {y}) 双击鼠标")
            self.last_click_pos = (x, y)
        except Exception as e:
            self.log(f"双击鼠标失败: {str(e)}")
            self.status_label.config(text="双击鼠标失败")
            messagebox.showerror("错误", f"双击鼠标失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseControlTester(root)
    root.mainloop() 