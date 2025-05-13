import os
import cv2
import numpy as np
from GameHelper import GameHelper
import time
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import traceback
import sys
import win32gui

class ScreenshotVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("游戏区域截图工具")
        
        # 设置窗口大小
        self.root.geometry("1200x800")
        
        # 初始化 GameHelper
        self.helper = GameHelper()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建左侧控制面板
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # 创建目标选择框
        self.target_frame = ttk.LabelFrame(self.control_frame, text="截图目标")
        self.target_frame.pack(pady=5, fill=tk.X)
        
        self.target_var = tk.StringVar(value="欢乐斗地主")
        self.target_radio1 = ttk.Radiobutton(self.target_frame, text="欢乐斗地主", variable=self.target_var, value="欢乐斗地主")
        self.target_radio1.pack(side=tk.LEFT, padx=5)
        self.target_radio2 = ttk.Radiobutton(self.target_frame, text="雷电模拟器", variable=self.target_var, value="雷电模拟器")
        self.target_radio2.pack(side=tk.LEFT, padx=5)
        
        # 创建截图按钮
        self.screenshot_button = ttk.Button(self.control_frame, text="截取游戏区域", command=self.take_screenshot)
        self.screenshot_button.pack(pady=5)
        
        # 创建保存路径选择框
        self.path_frame = ttk.LabelFrame(self.control_frame, text="保存路径")
        self.path_frame.pack(pady=5, fill=tk.X)
        
        # 使用绝对路径作为默认保存位置
        default_path = os.path.abspath("screenshots")
        self.path_var = tk.StringVar(value=default_path)
        self.path_entry = ttk.Entry(self.path_frame, textvariable=self.path_var, width=30)
        self.path_entry.pack(side=tk.LEFT, pady=5, padx=5, fill=tk.X, expand=True)
        
        self.browse_button = ttk.Button(self.path_frame, text="浏览", command=self.browse_path)
        self.browse_button.pack(side=tk.LEFT, pady=5, padx=5)
        
        # 创建状态标签
        self.status_label = ttk.Label(self.control_frame, text="就绪")
        self.status_label.pack(pady=5)
        
        # 创建图片显示区域
        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 初始化变量
        self.original_image = None
        self.photo_image = None
        self.scale_factor = 1.0
        self.image_position = (0, 0)
        
        # 打印当前工作目录和Python版本信息
        print(f"当前工作目录: {os.getcwd()}")
        print(f"Python版本: {sys.version}")
        print(f"OpenCV版本: {cv2.__version__}")
        print(f"默认保存路径: {default_path}")
        
    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)
            print(f"选择的保存路径: {path}")
            
    def find_window(self, title):
        """查找指定标题的窗口"""
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if title in window_title:
                    extra.append(hwnd)
            return True
        
        hwnd_list = []
        win32gui.EnumWindows(callback, hwnd_list)
        return hwnd_list[0] if hwnd_list else 0
            
    def take_screenshot(self):
        try:
            self.status_label.config(text="正在截图...")
            self.root.update()
            
            # 根据选择的目标设置窗口标题
            target = self.target_var.get()
            print(f"选择的目标: {target}")
            
            # 尝试查找窗口
            try:
                if target == "欢乐斗地主":
                    print("尝试查找欢乐斗地主窗口...")
                    hwnd = self.find_window("欢乐斗地主")
                else:
                    print("尝试查找雷电模拟器窗口...")
                    hwnd = self.find_window("雷电模拟器")
                
                if hwnd == 0:
                    error_msg = f"找不到{target}窗口，请确保窗口已打开"
                    print(error_msg)
                    messagebox.showerror("错误", error_msg)
                    self.status_label.config(text="找不到窗口")
                    return
                
                print(f"找到窗口，句柄: {hwnd}")
                
                # 设置GameHelper的窗口句柄
                self.helper.Handle = hwnd
                
            except Exception as e:
                error_msg = f"查找窗口时出错: {str(e)}"
                print(error_msg)
                messagebox.showerror("错误", error_msg)
                self.status_label.config(text="查找窗口失败")
                return
            
            # 截取整个游戏窗口
            print(f"开始截图 - 目标: {target}")
            try:
                screenshot = self.helper.Screenshot()
            except Exception as e:
                error_msg = f"截图时出错: {str(e)}"
                print(error_msg)
                messagebox.showerror("错误", error_msg)
                self.status_label.config(text="截图失败")
                return
            
            if screenshot is None:
                error_msg = f"截图失败，无法获取{target}窗口"
                print(error_msg)
                messagebox.showerror("错误", error_msg)
                self.status_label.config(text="截图失败")
                return
                
            print(f"截图成功，图像尺寸: {screenshot.size}")
            
            # 保存原始PIL图像
            save_path = self.path_var.get()
            print(f"准备保存到路径: {save_path}")
            
            # 确保路径存在
            try:
                if not os.path.exists(save_path):
                    print(f"创建目录: {save_path}")
                    os.makedirs(save_path)
                    print("目录创建成功")
            except Exception as e:
                print(f"创建目录失败: {e}")
                # 尝试使用当前目录
                save_path = os.getcwd()
                self.path_var.set(save_path)
                print(f"使用当前目录: {save_path}")
            
            # 生成文件名
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(save_path, f'{target}_{timestamp}.png')
            print(f"完整文件路径: {filename}")
            
            # 检查文件是否可写
            try:
                with open(filename, 'wb') as f:
                    pass
            except Exception as e:
                print(f"文件写入测试失败: {e}")
                # 尝试使用临时目录
                import tempfile
                save_path = tempfile.gettempdir()
                self.path_var.set(save_path)
                filename = os.path.join(save_path, f'{target}_{timestamp}.png')
                print(f"使用临时目录: {filename}")
            
            # 使用PIL保存图像
            print("开始保存图像...")
            try:
                screenshot.save(filename)
                print(f"截图已保存到: {filename}")
                messagebox.showinfo("成功", f"截图已保存到: {filename}")
                self.status_label.config(text=f"截图已保存: {os.path.basename(filename)}")
            except Exception as e:
                print(f"PIL保存失败: {e}")
                # 尝试使用OpenCV保存
                try:
                    # 转换为OpenCV格式
                    img = np.array(screenshot)
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    success = cv2.imwrite(filename, img)
                    if success:
                        print(f"OpenCV保存成功: {filename}")
                        messagebox.showinfo("成功", f"截图已保存到: {filename}")
                        self.status_label.config(text=f"截图已保存: {os.path.basename(filename)}")
                    else:
                        error_msg = f"保存截图失败: {filename}"
                        print(error_msg)
                        messagebox.showerror("错误", error_msg)
                        self.status_label.config(text="保存失败")
                except Exception as e2:
                    error_msg = f"OpenCV保存也失败: {e2}"
                    print(error_msg)
                    messagebox.showerror("错误", error_msg)
                    self.status_label.config(text="保存失败")
            
            # 显示图像
            try:
                img = np.array(screenshot)
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                self.display_image(img)
            except Exception as e:
                error_msg = f"显示图像时出错: {str(e)}"
                print(error_msg)
                messagebox.showerror("错误", error_msg)
                self.status_label.config(text="显示失败")
            
        except Exception as e:
            error_msg = f"截图过程中出错: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            messagebox.showerror("错误", error_msg)
            self.status_label.config(text="截图出错")
        
    def display_image(self, img):
        try:
            # 转换为PIL格式
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.original_image = Image.fromarray(img_rgb)
            
            # 计算缩放比例
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # 计算缩放比例，保持宽高比
            width_ratio = canvas_width / self.original_image.width
            height_ratio = canvas_height / self.original_image.height
            self.scale_factor = min(width_ratio, height_ratio)
            
            # 缩放图片
            new_width = int(self.original_image.width * self.scale_factor)
            new_height = int(self.original_image.height * self.scale_factor)
            resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 转换为PhotoImage
            self.photo_image = ImageTk.PhotoImage(resized_image)
            
            # 清除画布并显示新图片
            self.canvas.delete("all")
            
            # 计算图片在画布上的位置（左上角）
            self.image_position = (
                (canvas_width - new_width) // 2,
                (canvas_height - new_height) // 2
            )
            
            # 在画布上创建图片
            self.canvas.create_image(
                self.image_position[0],
                self.image_position[1],
                image=self.photo_image,
                anchor=tk.NW  # 使用左上角作为锚点
            )
            
            print(f"图片显示成功，尺寸: {new_width}x{new_height}")
            
        except Exception as e:
            error_msg = f"显示图片时出错: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            messagebox.showerror("错误", error_msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotVisualizer(root)
    root.mainloop() 