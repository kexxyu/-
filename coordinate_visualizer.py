import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import numpy as np
import re
import os
import cv2
import sys
import traceback

# 添加项目根目录到系统路径
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CoordinateVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("坐标可视化工具")
        
        # 设置窗口大小
        self.root.geometry("1200x800")
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建左侧控制面板
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # 创建图片加载按钮
        self.load_button = ttk.Button(self.control_frame, text="加载图片", command=self.load_image)
        self.load_button.pack(pady=5)
        
        # 创建坐标输入框
        self.coord_frame = ttk.LabelFrame(self.control_frame, text="坐标输入 (例如: 160, 497, 933, 80)")
        self.coord_frame.pack(pady=5, fill=tk.X)
        
        # 创建单个坐标输入框
        self.coord_entry = ttk.Entry(self.coord_frame, width=30)
        self.coord_entry.pack(pady=5, padx=5, fill=tk.X)
        
        # 创建绘制按钮
        self.draw_button = ttk.Button(self.control_frame, text="绘制框", command=self.draw_box)
        self.draw_button.pack(pady=5)
        
        # 创建清除按钮
        self.clear_button = ttk.Button(self.control_frame, text="清除框", command=self.clear_box)
        self.clear_button.pack(pady=5)
        
        # 创建保存路径选择按钮
        self.path_button = ttk.Button(self.control_frame, text="选择保存路径", command=self.select_save_path)
        self.path_button.pack(pady=5)
        
        # 创建保存路径显示标签
        self.path_label = ttk.Label(self.control_frame, text="保存路径: 未选择")
        self.path_label.pack(pady=5)
        
        # 创建截图按钮
        self.screenshot_button = ttk.Button(self.control_frame, text="保存选中区域", command=self.save_selected_area)
        self.screenshot_button.pack(pady=5)
        
        # 创建坐标显示标签
        self.coord_label = ttk.Label(self.control_frame, text="当前坐标: ")
        self.coord_label.pack(pady=5)
        
        # 在control_frame中添加识别按钮
        self.recognize_button = ttk.Button(self.control_frame, text="识别卡牌", command=self.recognize_cards)
        self.recognize_button.pack(pady=5)
        
        # 添加结果显示区域
        self.result_frame = ttk.LabelFrame(self.control_frame, text="识别结果")
        self.result_frame.pack(pady=5, fill=tk.X)
        
        self.result_text = tk.Text(self.result_frame, height=3, width=30)
        self.result_text.pack(pady=5, padx=5, fill=tk.X)
        
        # 创建图片显示区域
        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 初始化变量
        self.original_image = None
        self.photo_image = None
        self.scale_factor = 1.0
        self.boxes = []
        self.image_position = (0, 0)  # 图片在画布上的位置
        self.save_path = None  # 保存路径
        
        # 鼠标拖动相关变量
        self.start_x = None
        self.start_y = None
        self.current_rect = None
        self.is_drawing = False
        
        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        
    def start_draw(self, event):
        if not self.original_image:
            return
            
        # 检查点击是否在图片范围内
        if (event.x < self.image_position[0] or 
            event.x > self.image_position[0] + self.original_image.width * self.scale_factor or
            event.y < self.image_position[1] or 
            event.y > self.image_position[1] + self.original_image.height * self.scale_factor):
            return
            
        self.start_x = event.x
        self.start_y = event.y
        self.is_drawing = True
        
        # 创建新的矩形
        self.current_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2
        )
        
    def draw(self, event):
        if not self.is_drawing or not self.current_rect:
            return
            
        # 更新矩形
        self.canvas.coords(self.current_rect, 
                          self.start_x, self.start_y, event.x, event.y)
        
        # 计算实际坐标（相对于图片）
        x1 = (min(self.start_x, event.x) - self.image_position[0]) / self.scale_factor
        y1 = (min(self.start_y, event.y) - self.image_position[1]) / self.scale_factor
        x2 = (max(self.start_x, event.x) - self.image_position[0]) / self.scale_factor
        y2 = (max(self.start_y, event.y) - self.image_position[1]) / self.scale_factor
        
        # 计算宽度和高度
        width = x2 - x1
        height = y2 - y1
        
        # 更新坐标显示
        self.coord_label.config(text=f"当前坐标: ({int(x1)}, {int(y1)}, {int(width)}, {int(height)})")
        
    def end_draw(self, event):
        if not self.is_drawing or not self.current_rect:
            return
            
        # 计算最终坐标
        x1 = (min(self.start_x, event.x) - self.image_position[0]) / self.scale_factor
        y1 = (min(self.start_y, event.y) - self.image_position[1]) / self.scale_factor
        x2 = (max(self.start_x, event.x) - self.image_position[0]) / self.scale_factor
        y2 = (max(self.start_y, event.y) - self.image_position[1]) / self.scale_factor
        
        width = x2 - x1
        height = y2 - y1
        
        # 更新坐标输入框
        self.coord_entry.delete(0, tk.END)
        self.coord_entry.insert(0, f"{int(x1)}, {int(y1)}, {int(width)}, {int(height)}")
        
        # 保存框的引用
        self.boxes.append(self.current_rect)
        
        # 重置变量
        self.is_drawing = False
        self.current_rect = None
        self.start_x = None
        self.start_y = None
        
    def load_image(self):
        # 打开文件对话框
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        
        if file_path:
            # 加载图片
            self.original_image = Image.open(file_path)
            
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
            
            # 清除之前的框
            self.boxes = []
            
    def draw_box(self):
        if not self.original_image:
            return
            
        try:
            # 获取坐标字符串
            coord_str = self.coord_entry.get().strip()
            
            # 使用正则表达式提取数字
            numbers = re.findall(r'\d+', coord_str)
            
            if len(numbers) < 4:
                messagebox.showerror("错误", "请输入完整的坐标，例如: 160, 497, 933, 80")
                return
                
            # 提取坐标值
            x = int(numbers[0])
            y = int(numbers[1])
            width = int(numbers[2])
            height = int(numbers[3])
            
            # 计算右下角坐标
            x2 = x + width
            y2 = y + height
            
            # 应用缩放因子
            scaled_x = x * self.scale_factor
            scaled_y = y * self.scale_factor
            scaled_x2 = x2 * self.scale_factor
            scaled_y2 = y2 * self.scale_factor
            
            # 计算框在画布上的位置
            box_x1 = self.image_position[0] + scaled_x
            box_y1 = self.image_position[1] + scaled_y
            box_x2 = self.image_position[0] + scaled_x2
            box_y2 = self.image_position[1] + scaled_y2
            
            # 绘制矩形框
            box = self.canvas.create_rectangle(
                box_x1, box_y1, box_x2, box_y2,
                outline='red',
                width=2
            )
            
            # 保存框的引用
            self.boxes.append(box)
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字坐标")
            
    def clear_box(self):
        # 清除所有框
        for box in self.boxes:
            self.canvas.delete(box)
        self.boxes = []
        # 清除坐标输入框
        self.coord_entry.delete(0, tk.END)
        # 清除坐标显示
        self.coord_label.config(text="当前坐标: ")

    def select_save_path(self):
        """选择保存路径"""
        self.save_path = filedialog.askdirectory()
        if self.save_path:
            self.path_label.config(text=f"保存路径: {self.save_path}")

    def save_selected_area(self):
        """保存选中区域"""
        if not self.original_image or not self.save_path:
            messagebox.showerror("错误", "请先加载图片并选择保存路径")
            return
            
        try:
            # 获取坐标字符串
            coord_str = self.coord_entry.get().strip()
            numbers = re.findall(r'\d+', coord_str)
            
            if len(numbers) < 4:
                messagebox.showerror("错误", "请先绘制选择框")
                return
                
            # 提取坐标值
            x = int(numbers[0])
            y = int(numbers[1])
            width = int(numbers[2])
            height = int(numbers[3])
            
            # 计算右下角坐标
            x2 = x + width
            y2 = y + height
            
            # 裁剪图片
            cropped_image = self.original_image.crop((x, y, x2, y2))
            
            # 生成文件名（使用时间戳）
            import time
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.save_path, filename)
            
            # 保存图片
            cropped_image.save(filepath)
            messagebox.showinfo("成功", f"截图已保存到: {filepath}")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存截图时出错: {str(e)}")

    def recognize_cards(self):
        """识别选中区域的卡牌"""
        if not self.original_image:
            messagebox.showerror("错误", "请先加载图片")
            return
        
        try:
            # 获取坐标字符串
            coord_str = self.coord_entry.get().strip()
            numbers = re.findall(r'\d+', coord_str)
            
            if len(numbers) < 4:
                messagebox.showerror("错误", "请先绘制选择框")
                return
            
            # 提取坐标值
            x = int(numbers[0])
            y = int(numbers[1])
            width = int(numbers[2])
            height = int(numbers[3])
            
            # 裁剪图片
            cropped_image = self.original_image.crop((x, y, x + width, y + height))
            
            # 转换为OpenCV格式
            img = cv2.cvtColor(np.array(cropped_image), cv2.COLOR_RGB2BGR)
            
            # 导入必要的模块
            from main import cards_info, GameHelper, helper
            
            # 确保GameHelper已初始化
            if not hasattr(helper, 'PicsCV'):
                GameHelper()
                
            # 调用cards_info函数
            result = cards_info(img, (0, 0, width, height))
            
            # 显示结果
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"识别结果: {result}")
            
        except Exception as e:
            messagebox.showerror("错误", f"识别失败: {str(e)}")
            traceback.print_exc()  # 打印详细的错误信息

if __name__ == "__main__":
    root = tk.Tk()
    app = CoordinateVisualizer(root)
    root.mainloop() 