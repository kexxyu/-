import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import time
import os
from PIL import Image, ImageTk
import numpy as np

class ImageCoordinateTool:
    def __init__(self, root):
        self.root = root
        self.root.title("图片坐标测量工具")
        self.root.geometry("1200x800")  # 增加窗口默认大小
        self.root.resizable(True, True)
        
        # 创建保存坐标的文件夹
        if not os.path.exists('coordinates'):
            os.makedirs('coordinates')
        
        # 初始化变量
        self.image_path = None
        self.original_image = None
        self.display_image = None
        self.photo = None
        self.coordinates = []  # 存储坐标和名称的列表，格式为 [(x, y, name), ...]
        self.is_recording = False
        self.last_mouse_pos = (0, 0)
        self.scale_factor = 1.0
        self.zoom_factor = 1.0  # 缩放因子
        self.coordinate_file = 'coordinates/all_coordinates.txt'  # 固定的坐标文件路径
        
        # 创建界面元素
        self.create_widgets()
        
        # 开始更新鼠标位置
        self.update_mouse_position()
        
        # 绑定快捷键
        self.bind_shortcuts()
    
    def create_widgets(self):
        # 创建样式
        style = ttk.Style()
        style.configure("TButton", font=("微软雅黑", 10))
        style.configure("TLabel", font=("微软雅黑", 10))
        style.configure("TEntry", font=("微软雅黑", 10))
        
        # 创建标题
        title_label = ttk.Label(self.root, text="凯旋棋牌坐标测量工具", font=("微软雅黑", 14, "bold"))
        title_label.pack(pady=10)
        
        # 创建按钮区域
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=20, pady=5)
        
        # 加载图片按钮
        load_btn = ttk.Button(button_frame, text="加载图片", command=self.load_image)
        load_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # 清除坐标按钮
        clear_btn = ttk.Button(button_frame, text="清除坐标", command=self.clear_coordinates)
        clear_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # 保存坐标按钮
        save_btn = ttk.Button(button_frame, text="保存坐标", command=self.save_coordinates)
        save_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # 创建缩放控制区域
        zoom_frame = ttk.Frame(self.root)
        zoom_frame.pack(fill="x", padx=20, pady=5)
        
        ttk.Label(zoom_frame, text="缩放:").pack(side="left", padx=5)
        
        # 缩小按钮
        zoom_out_btn = ttk.Button(zoom_frame, text="-", width=3, command=self.zoom_out)
        zoom_out_btn.pack(side="left", padx=5)
        
        # 缩放比例显示
        self.zoom_label = ttk.Label(zoom_frame, text="100%")
        self.zoom_label.pack(side="left", padx=5)
        
        # 放大按钮
        zoom_in_btn = ttk.Button(zoom_frame, text="+", width=3, command=self.zoom_in)
        zoom_in_btn.pack(side="left", padx=5)
        
        # 重置缩放按钮
        reset_zoom_btn = ttk.Button(zoom_frame, text="重置缩放", command=self.reset_zoom)
        reset_zoom_btn.pack(side="left", padx=5)
        
        # 创建鼠标位置显示区域
        mouse_frame = ttk.LabelFrame(self.root, text="鼠标位置", padding=10)
        mouse_frame.pack(fill="x", padx=20, pady=5)
        
        # 图片坐标
        image_frame = ttk.Frame(mouse_frame)
        image_frame.pack(fill="x", pady=5)
        ttk.Label(image_frame, text="图片坐标:").pack(side="left", padx=5)
        self.image_pos_label = ttk.Label(image_frame, text="(0, 0)")
        self.image_pos_label.pack(side="left", padx=5)
        
        # 创建图片显示区域
        self.image_canvas = tk.Canvas(self.root, bg="white")
        self.image_canvas.pack(fill="both", expand=True, padx=20, pady=5)
        
        # 绑定鼠标事件
        self.image_canvas.bind("<Motion>", self.on_mouse_move)
        self.image_canvas.bind("<Button-1>", self.on_mouse_click)
        self.image_canvas.bind("<MouseWheel>", self.on_mouse_wheel)  # 绑定鼠标滚轮事件
        
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
        
        # 添加快捷键提示
        shortcut_label = ttk.Label(status_frame, text="快捷键: Ctrl+S 保存坐标 | Ctrl+C 清除坐标 | 鼠标滚轮缩放")
        shortcut_label.pack(side="right")
    
    def bind_shortcuts(self):
        """绑定快捷键"""
        self.root.bind("<Control-s>", lambda event: self.save_coordinates())
        self.root.bind("<Control-c>", lambda event: self.clear_coordinates())
        self.root.bind("<Control-plus>", lambda event: self.zoom_in())
        self.root.bind("<Control-minus>", lambda event: self.zoom_out())
        self.root.bind("<Control-0>", lambda event: self.reset_zoom())
    
    def load_image(self):
        """加载图片"""
        file_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        
        if not file_path:
            return
        
        try:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            
            # 重置缩放因子
            self.zoom_factor = 1.0
            self.zoom_label.config(text="100%")
            
            # 调整图片大小以适应显示区域
            self.display_image = self.resize_image(self.original_image)
            self.photo = ImageTk.PhotoImage(self.display_image)
            
            # 更新画布大小
            self.image_canvas.config(width=self.display_image.width, height=self.display_image.height)
            self.image_canvas.create_image(0, 0, anchor="nw", image=self.photo)
            
            # 计算缩放因子
            self.scale_factor = self.original_image.width / self.display_image.width
            
            # 检查坐标文件是否存在，如果不存在则创建
            if not os.path.exists(self.coordinate_file):
                with open(self.coordinate_file, 'w', encoding='utf-8') as f:
                    f.write("# 凯旋棋牌坐标数据\n")
                    f.write("# 格式: 名称: (x, y) - 相对于图片左上角的坐标\n")
                    f.write("# 时间: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                    f.write("\n")
            
            self.status_label.config(text=f"已加载图片: {os.path.basename(file_path)}")
        except Exception as e:
            self.status_label.config(text=f"加载图片失败: {str(e)}")
            messagebox.showerror("错误", f"加载图片失败: {str(e)}")
    
    def resize_image(self, image):
        """调整图片大小以适应显示区域"""
        # 获取画布大小
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        
        # 如果画布大小无效，使用默认值
        if canvas_width <= 1:
            canvas_width = 1000  # 增加默认宽度
        if canvas_height <= 1:
            canvas_height = 600  # 增加默认高度
        
        # 计算缩放比例
        width, height = image.size
        scale = min(canvas_width / width, canvas_height / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # 应用用户设置的缩放因子
        new_width = int(new_width * self.zoom_factor)
        new_height = int(new_height * self.zoom_factor)
        
        # 缩放图像
        return image.resize((new_width, new_height), Image.LANCZOS)
    
    def zoom_in(self):
        """放大图片"""
        if self.original_image:
            self.zoom_factor *= 1.2
            self.update_image()
            self.zoom_label.config(text=f"{int(self.zoom_factor * 100)}%")
    
    def zoom_out(self):
        """缩小图片"""
        if self.original_image:
            self.zoom_factor /= 1.2
            self.update_image()
            self.zoom_label.config(text=f"{int(self.zoom_factor * 100)}%")
    
    def reset_zoom(self):
        """重置缩放"""
        if self.original_image:
            self.zoom_factor = 1.0
            self.update_image()
            self.zoom_label.config(text="100%")
    
    def update_image(self):
        """更新图片显示"""
        if self.original_image:
            self.display_image = self.resize_image(self.original_image)
            self.photo = ImageTk.PhotoImage(self.display_image)
            
            # 更新画布大小
            self.image_canvas.config(width=self.display_image.width, height=self.display_image.height)
            self.image_canvas.delete("all")
            self.image_canvas.create_image(0, 0, anchor="nw", image=self.photo)
            
            # 更新缩放因子
            self.scale_factor = self.original_image.width / self.display_image.width
    
    def on_mouse_wheel(self, event):
        """鼠标滚轮事件处理"""
        if self.original_image:
            if event.delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
    
    def on_mouse_move(self, event):
        """鼠标移动事件处理"""
        if self.original_image:
            # 获取鼠标在画布上的坐标
            canvas_x, canvas_y = event.x, event.y
            
            # 计算鼠标在原始图片上的坐标
            original_x = int(canvas_x * self.scale_factor)
            original_y = int(canvas_y * self.scale_factor)
            
            # 更新坐标显示
            self.image_pos_label.config(text=f"({original_x}, {original_y})")
    
    def on_mouse_click(self, event):
        """鼠标点击事件处理"""
        if self.original_image:
            # 获取鼠标在画布上的坐标
            canvas_x, canvas_y = event.x, event.y
            
            # 计算鼠标在原始图片上的坐标
            original_x = int(canvas_x * self.scale_factor)
            original_y = int(canvas_y * self.scale_factor)
            
            # 弹出对话框让用户为坐标命名
            name = simpledialog.askstring("坐标命名", "请为这个坐标命名:", initialvalue="")
            
            if name:
                # 记录坐标和名称
                self.coordinates.append((original_x, original_y, name))
                self.coord_listbox.insert(tk.END, f"{name}: ({original_x}, {original_y})")
                self.coord_listbox.see(tk.END)
                
                # 立即保存到文件
                self.save_coordinate_to_file(original_x, original_y, name)
    
    def save_coordinate_to_file(self, x, y, name):
        """将单个坐标保存到文件"""
        # 检查坐标文件是否存在，如果不存在则创建
        if not os.path.exists(self.coordinate_file):
            with open(self.coordinate_file, 'w', encoding='utf-8') as f:
                f.write("# 凯旋棋牌坐标数据\n")
                f.write("# 格式: 名称: (x, y) - 相对于图片左上角的坐标\n")
                f.write("# 时间: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                f.write("\n")
        
        # 追加坐标到文件
        with open(self.coordinate_file, 'a', encoding='utf-8') as f:
            f.write(f"{name}: ({x}, {y})\n")
    
    def update_mouse_position(self):
        """更新鼠标位置信息"""
        # 每秒更新10次
        self.root.after(100, self.update_mouse_position)
    
    def clear_coordinates(self):
        """清除记录的坐标"""
        self.coordinates = []
        self.coord_listbox.delete(0, tk.END)
        self.status_label.config(text="已清除所有坐标")
    
    def save_coordinates(self):
        """保存当前鼠标位置的坐标"""
        if not self.original_image:
            messagebox.showinfo("提示", "请先加载图片")
            return
        
        # 获取当前鼠标位置
        x, y = self.image_pos_label.cget("text").strip("()").split(",")
        x, y = int(x), int(y)
        
        # 弹出对话框让用户为坐标命名
        name = simpledialog.askstring("坐标命名", "请为这个坐标命名:", initialvalue="")
        
        if name:
            # 记录坐标和名称
            self.coordinates.append((x, y, name))
            self.coord_listbox.insert(tk.END, f"{name}: ({x}, {y})")
            self.coord_listbox.see(tk.END)
            
            # 保存到文件
            self.save_coordinate_to_file(x, y, name)
            
            self.status_label.config(text=f"已保存坐标: {name}: ({x}, {y})")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCoordinateTool(root)
    root.mainloop() 