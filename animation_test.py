import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2

class AnimationTester:
    def __init__(self, root):
        self.root = root
        self.root.title("动画检测测试工具")
        
        # 设置窗口大小
        self.root.geometry("1400x800")
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建左侧控制面板
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # 创建图片加载按钮
        self.load_frame = ttk.LabelFrame(self.control_frame, text="图片加载")
        self.load_frame.pack(pady=5, fill=tk.X)
        
        self.load_btn1 = ttk.Button(self.load_frame, text="加载第一张图片", command=lambda: self.load_image(1))
        self.load_btn1.pack(pady=5, padx=5, fill=tk.X)
        
        self.load_btn2 = ttk.Button(self.load_frame, text="加载第二张图片", command=lambda: self.load_image(2))
        self.load_btn2.pack(pady=5, padx=5, fill=tk.X)
        
        # 创建坐标输入框
        self.coord_frame = ttk.LabelFrame(self.control_frame, text="动画检测区域坐标")
        self.coord_frame.pack(pady=5, fill=tk.X)
        
        # 下家动画位置
        self.down_frame = ttk.Frame(self.coord_frame)
        self.down_frame.pack(pady=5, fill=tk.X)
        ttk.Label(self.down_frame, text="下家动画:").pack(side=tk.LEFT)
        self.down_coord = ttk.Entry(self.down_frame, width=30)
        self.down_coord.pack(side=tk.LEFT, padx=5)
        self.down_coord.insert(0, "853, 142, 871, 160")
        
        # 上家动画位置
        self.up_frame = ttk.Frame(self.coord_frame)
        self.up_frame.pack(pady=5, fill=tk.X)
        ttk.Label(self.up_frame, text="上家动画:").pack(side=tk.LEFT)
        self.up_coord = ttk.Entry(self.up_frame, width=30)
        self.up_coord.pack(side=tk.LEFT, padx=5)
        self.up_coord.insert(0, "431, 142, 448, 160")
        
        # 自己动画位置
        self.self_frame = ttk.Frame(self.coord_frame)
        self.self_frame.pack(pady=5, fill=tk.X)
        ttk.Label(self.self_frame, text="自己动画:").pack(side=tk.LEFT)
        self.self_coord = ttk.Entry(self.self_frame, width=30)
        self.self_coord.pack(side=tk.LEFT, padx=5)
        self.self_coord.insert(0, "622, 330, 640, 373")
        
        # 创建比较按钮
        self.compare_btn = ttk.Button(self.control_frame, text="比较图片", command=self.compare_images)
        self.compare_btn.pack(pady=5)
        
        # 创建结果显示区域
        self.result_frame = ttk.LabelFrame(self.control_frame, text="比较结果")
        self.result_frame.pack(pady=5, fill=tk.X)
        
        self.result_text = tk.Text(self.result_frame, height=10, width=40)
        self.result_text.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        
        # 创建图片显示区域
        self.image_frame = ttk.Frame(self.main_frame)
        self.image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 第一张图片显示
        self.canvas1_frame = ttk.LabelFrame(self.image_frame, text="第一张图片")
        self.canvas1_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.canvas1 = tk.Canvas(self.canvas1_frame, bg='white')
        self.canvas1.pack(fill=tk.BOTH, expand=True)
        
        # 第二张图片显示
        self.canvas2_frame = ttk.LabelFrame(self.image_frame, text="第二张图片")
        self.canvas2_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.canvas2 = tk.Canvas(self.canvas2_frame, bg='white')
        self.canvas2.pack(fill=tk.BOTH, expand=True)
        
        # 初始化变量
        self.image1 = None
        self.image2 = None
        self.photo1 = None
        self.photo2 = None
        self.scale_factor1 = 1.0
        self.scale_factor2 = 1.0
        self.image_position1 = (0, 0)
        self.image_position2 = (0, 0)
        
    def load_image(self, image_num):
        # 打开文件对话框
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        
        if file_path:
            # 加载图片
            image = Image.open(file_path)
            
            if image_num == 1:
                self.image1 = image
                canvas = self.canvas1
                self.scale_factor1 = self.calculate_scale_factor(image, canvas)
                self.display_image(image, canvas, self.scale_factor1, 1)
            else:
                self.image2 = image
                canvas = self.canvas2
                self.scale_factor2 = self.calculate_scale_factor(image, canvas)
                self.display_image(image, canvas, self.scale_factor2, 2)
    
    def calculate_scale_factor(self, image, canvas):
        # 计算缩放比例
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        # 计算缩放比例，保持宽高比
        width_ratio = canvas_width / image.width
        height_ratio = canvas_height / image.height
        return min(width_ratio, height_ratio)
    
    def display_image(self, image, canvas, scale_factor, image_num):
        # 缩放图片
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 转换为PhotoImage
        photo = ImageTk.PhotoImage(resized_image)
        
        # 清除画布并显示新图片
        canvas.delete("all")
        
        # 计算图片在画布上的位置（左上角）
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        image_position = (
            (canvas_width - new_width) // 2,
            (canvas_height - new_height) // 2
        )
        
        # 在画布上创建图片
        canvas.create_image(
            image_position[0],
            image_position[1],
            image=photo,
            anchor=tk.NW
        )
        
        # 保存引用
        if image_num == 1:
            self.photo1 = photo
            self.image_position1 = image_position
        else:
            self.photo2 = photo
            self.image_position2 = image_position
    
    def parse_coordinates(self, coord_str):
        try:
            # 分割坐标字符串
            coords = [int(x.strip()) for x in coord_str.split(',')]
            if len(coords) != 4:
                raise ValueError("坐标格式错误")
            return coords
        except Exception as e:
            messagebox.showerror("错误", f"坐标格式错误: {str(e)}")
            return None
    
    def compare_images(self):
        if not self.image1 or not self.image2:
            messagebox.showerror("错误", "请先加载两张图片")
            return
        
        # 清空结果显示
        self.result_text.delete(1.0, tk.END)
        
        # 获取坐标
        down_coords = self.parse_coordinates(self.down_coord.get())
        up_coords = self.parse_coordinates(self.up_coord.get())
        self_coords = self.parse_coordinates(self.self_coord.get())
        
        if not all([down_coords, up_coords, self_coords]):
            return
        
        # 转换图片为numpy数组
        img1_array = np.array(self.image1)
        img2_array = np.array(self.image2)
        
        # 比较每个区域
        regions = [
            ("下家动画区域", down_coords),
            ("上家动画区域", up_coords),
            ("自己动画区域", self_coords)
        ]
        
        for region_name, coords in regions:
            x, y, w, h = coords
            # 提取区域
            region1 = img1_array[y:y+h, x:x+w]
            region2 = img2_array[y:y+h, x:x+w]
            
            # 计算差异
            diff = np.abs(region1.astype(float) - region2.astype(float))
            diff_percentage = (np.sum(diff > 0) / diff.size) * 100
            
            # 显示结果
            result = f"{region_name}:\n"
            result += f"坐标: ({x}, {y}, {w}, {h})\n"
            result += f"差异百分比: {diff_percentage:.2f}%\n"
            result += f"{'有动画' if diff_percentage > 5 else '无动画'}\n\n"
            
            self.result_text.insert(tk.END, result)
            
            # 在图片上绘制检测区域
            self.draw_region(self.canvas1, coords, self.scale_factor1, self.image_position1)
            self.draw_region(self.canvas2, coords, self.scale_factor2, self.image_position2)
    
    def draw_region(self, canvas, coords, scale_factor, image_position):
        x, y, w, h = coords
        # 计算缩放后的坐标
        scaled_x = image_position[0] + x * scale_factor
        scaled_y = image_position[1] + y * scale_factor
        scaled_w = w * scale_factor
        scaled_h = h * scale_factor
        
        # 绘制矩形
        canvas.create_rectangle(
            scaled_x, scaled_y,
            scaled_x + scaled_w, scaled_y + scaled_h,
            outline='red',
            width=2
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimationTester(root)
    root.mainloop() 