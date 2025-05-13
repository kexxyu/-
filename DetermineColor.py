# 导入OpenCV库用于图像处理
import cv2
# 导入numpy库用于数值计算
import numpy as np


# 定义颜色分类类
class ColorClassify(object):
    # 初始化函数,设置debug模式
    def __init__(self, debug=True):
        self.debug = debug
        # 颜色范围，主要参考HSV颜色分量分布表：
        # 其中，gray和white进行了平衡中线调整，使白色占比更大些
        # 定义HSV颜色空间中各种颜色的范围
        self.hsv_color = {
            # 灰色的HSV范围
            "Gray": [(0, 180), (0, 43), (46, 150)],
            # 白色的HSV范围
            "White": [(0, 180), (0, 30), (151, 255)],
            # 红色的HSV范围(由于红色横跨色相环两端,需要两个范围)
            "Red": [[(0, 10), (156, 180)], (43, 255), (46, 255)],
            # 橙色的HSV范围
            "Orange": [(11, 25), (43, 255), (46, 255)],
            # 绿色的HSV范围
            "Green": [(35, 77), (43, 255), (46, 255)],
            # 蓝色的HSV范围
            "Blue": [(100, 124), (43, 255), (46, 255)],
        }

        # 注释掉的完整颜色范围定义,包含更多颜色
        """{
            "Black": [(0, 180), (0, 255), (0, 46)],
            "Gray": [(0, 180), (0, 43), (46, 150)],
            "White": [(0, 180), (0, 30), (151, 255)],
            "Red": [[(0, 10), (156, 180)], (43, 255), (46, 255)],
            "Orange": [(11, 25), (43, 255), (46, 255)],
            "Yellow": [(26, 34), (43, 255), (46, 255)],
            "Green": [(35, 77), (43, 255), (46, 255)],
            "CyanBlue": [(78, 99), (43, 255), (46, 255)],
            "Blue": [(100, 124), (43, 255), (46, 255)],
            "Purple": [(125, 155), (43, 255), (46, 255)]
        }"""

    # 获取HSV图像的直方图
    def get_hsv_hist(self, img_hsv):
        # 分离HSV三个通道
        h, s, v = img_hsv[:, :, 0], img_hsv[:, :, 1], img_hsv[:, :, 2]

        # 定义H通道的直方图区间
        h_bins = [0, 11, 26, 35, 78, 100, 125, 156, 180]
        # 计算H通道直方图
        h_hist = np.histogram(h, h_bins)
        # 定义S通道的直方图区间
        s_bins = [0, 30, 43, 255]
        # 计算S通道直方图
        s_hist = np.histogram(s, s_bins)
        # 定义V通道的直方图区间
        v_bins = [0, 46, 151, 255]
        # 计算V通道直方图
        v_hist = np.histogram(v, v_bins)

        # 返回三个通道的直方图
        return [h_hist, s_hist, v_hist]

    # 获取HSV直方图的详细信息
    def get_hsv_info(self, h_hist, s_hist, v_hist):
        # 初始化信息字典
        infos = {
            "h": {
                "hist": h_hist,
                "argsort": None,
                "sort_normal": None,
                "arg_values": [],
            },
            "s": {
                "hist": s_hist,
                "argsort": None,
                "sort_normal": None,
                "arg_values": [],
            },
            "v": {
                "hist": v_hist,
                "argsort": None,
                "sort_normal": None,
                "arg_values": [],
            }
        }
        # 遍历HSV三个通道
        for k in infos:
            # 获取当前通道的直方图
            hist = infos[k]['hist']
            # 获取直方图中最大的两个值的索引
            argsort = np.argsort(hist[0])[::-1][:2]  # 逆序排列, 取前面最大的两个
            # 保存索引
            infos[k]['argsort'] = argsort
            # 计算归一化的排序值
            infos[k]['sort_normal'] = hist[0][argsort] / (sum(hist[0]) * 3)
            # 计算每个区间的平均值
            for idx in argsort:
                value_mean = round(np.mean([hist[1][idx], hist[1][idx + 1]]))
                infos[k]['arg_values'].append(value_mean)
        # 返回处理后的信息
        return infos

    # 获取HSV主要信息
    def get_hsv_main_info(self, h_hist, s_hist, v_hist):
        # 获取H通道最大值的索引和对应区间
        h_main_idx = np.argmax(h_hist[0])
        h_main = [h_hist[1][h_main_idx], h_hist[1][h_main_idx + 1]]

        # 设置S通道权重并计算最大值
        s_weights = np.array([1, 1, 1])
        s_array = s_hist[0] * s_weights
        s_main_idx = np.argmax(s_array)
        s_main = [s_hist[1][s_main_idx], s_hist[1][s_main_idx + 1]]

        # 设置V通道权重并计算最大值
        v_weights = np.array([1, 1, 1])
        v_array = v_hist[0] * v_weights
        v_main_idx = np.argmax(v_array)
        v_main = [v_hist[1][v_main_idx], v_hist[1][v_main_idx + 1]]

        # 如果是debug模式,打印信息
        if self.debug:
            print("h_hist: {}\ns_hist: {}\nv_hist: {}".format(h_hist, s_hist, v_hist))
            print("h_main: {}, s_main: {}, v_main: {}".format(h_main, s_main, v_main))
        # 返回三个通道的平均值
        return np.mean(h_main), np.mean(s_main), np.mean(v_main)

    # HSV值转换为颜色名称
    def hsv2color(self, infos):
        # 获取HSV三个通道的信息
        h_info = infos['h']
        s_info = infos['s']
        v_info = infos['v']
        # 初始化结果字典
        result = {}
        # 遍历所有可能的HSV组合
        for snh, avh in zip(h_info['sort_normal'], h_info['arg_values']):
            for sns, avs in zip(s_info['sort_normal'], s_info['arg_values']):
                for snv, avv in zip(v_info['sort_normal'], v_info['arg_values']):
                    # 获取对应的颜色类别
                    cls = self.hsv2color_one(avh, avs, avv)
                    if cls is None:
                        pass
                        # print(avh, avs, avv)
                        continue
                    # 计算得分
                    score = snh + sns + snv
                    # 更新结果字典
                    if cls in result.keys():
                        result[cls] = max(score, result[cls])
                    else:
                        result[cls] = score
        # 返回按得分排序的结果
        return sorted(result.items(), key=lambda kv: (kv[1], kv[0]))[::-1]

    # 单个HSV值转换为颜色名称
    def hsv2color_one(self, h_mean, s_mean, v_mean):
        # 遍历所有预定义的颜色范围
        for cls, value in self.hsv_color.items():
            # 判断H值是否在范围内(红色需要特殊处理)
            if isinstance(value[0], list):
                h_flag = value[0][0][0] <= h_mean <= value[0][0][1] or value[0][1][0] <= h_mean <= value[0][1][1]
            else:
                h_flag = value[0][0] <= h_mean <= value[0][1]
            # 判断S值是否在范围内
            s_flag = value[1][0] <= s_mean <= value[1][1]
            # 判断V值是否在范围内
            v_flag = value[2][0] <= v_mean <= value[2][1]
            # 如果都在范围内,返回颜色名称
            if h_flag and s_flag and v_flag:
                return cls
        # 如果都不匹配,返回None
        return None

    # 图像颜色分类的主函数
    def classify(self, img):
        # 将BGR图像转换为HSV
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # 获取HSV直方图
        h_hist, s_hist, v_hist = self.get_hsv_hist(img_hsv)

        # 仅用hsv每个分量的最大值
        # h_mean, s_mean, v_mean = self.get_hsv_main_info(h_hist, s_hist, v_hist)
        # return self.hsv2color_one(h_mean, s_mean, v_mean)

        # 获取HSV信息并返回颜色分类结果
        infos = self.get_hsv_info(h_hist, s_hist, v_hist)
        return self.hsv2color(infos)


# 主程序入口
if __name__ == "__main__":
    # 创建颜色分类器实例
    classifier = ColorClassify(debug=True)
    # 读取测试图片
    img = cv2.imread("pics/ob8.png")
    # 进行颜色分类
    result = classifier.classify(img)
    # 打印分类结果
    print(result)
    # 获取第二个最可能的颜色及其得分
    cls, score = result[1]
    # 遍历所有结果
    for i in result:
        # 打印颜色名称
        print(i[0])
        # 如果是红色,打印其得分
        if i[0] == "Red":
            print(i[1])
