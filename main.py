# -*- coding: utf-8 -*-   测试用 测试在a分支的gitdsadasdasdasd
# @Time : 2024/3/6 0:36
# @Author : MaYun
# @File : best.py
# @Software: PyCharm
import GameHelper as gh
from GameHelper import GameHelper, play_sound, read_json, write_json, subtract_strings
import DetermineColor as DC
from collections import defaultdict
from douzero.env.move_detector import get_move_type
import sys
import time
import cv2
import numpy as np
from Recognition import yolo_detect
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from MainWindow import Ui_Form
from log_utils import trace_function  # 导入日志追踪装饰器

from douzero.env.game import GameEnv
from douzero.evaluation.deep_agent import DeepAgent
import traceback
from skimage.metrics import structural_similarity as ssim

import BidModel
import LandlordModel
import FarmerModel

RealCard2EnvCard = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
                    'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 17, 'X': 20, 'D': 30}

EnvCard2RealCard = {3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'T',
                    11: 'J', 12: 'Q', 13: 'K', 14: 'A', 17: '2', 20: 'X', 30: 'D'}

AllCards = ['D', 'X', '2', 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3']

AllEnvCard = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10,
              11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14, 17, 17, 17, 17, 20, 30]

helper = GameHelper()


@trace_function
def yolo_info(pos: tuple):
    img = helper.Screenshot()
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    # img = cv2.imread("2.png")
    img = img[pos[1]:pos[1] + pos[3], pos[0]:pos[0] + pos[2]]
    img, class_list, pos_list = yolo_detect(img)
    if class_list is not None:
        pos_list = [[sublist[0] + pos[0], sublist[1] + pos[1]] + sublist[2:] for sublist in pos_list]
    return img, class_list, pos_list


@trace_function
def compareImage(img1, img2):
    # 转换为灰度图
    gray1 = cv2.cvtColor(np.asarray(img1), cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(np.asarray(img2), cv2.COLOR_BGR2GRAY)

    # 使用结构相似性指数（SSIM）比较相似度
    ssim_index, _ = ssim(gray1, gray2, full=True)
    if ssim_index < 0.99:
        return True

    return False


@trace_function
def real_to_env(cards):
    env_card = [RealCard2EnvCard[c] for c in cards]
    env_card.sort()
    return env_card


@trace_function
def cards_filter(location, distance):  # 牌检测结果滤波
    if len(location) == 0:
        return 0
    locList = [location[0][0]]
    poslist = [location[0]]
    count = 1
    for e in location:
        flag = 1
        for have in locList:
            if abs(e[0] - have) <= distance:
                flag = 0
                break
        if flag:
            count += 1
            locList.append(e[0])
            poslist.append(e)
    return count, poslist


@trace_function
def find_pic(path: str, pos: tuple, click=False):
    # 在指定区域查找图片,path为图片路径,pos为查找区域
    result = helper.LocateOnScreen(path, pos)
    # 如果找到图片且需要点击
    if result and click:
        # 点击找到的位置
        helper.LeftClick(result)
    # 返回查找结果
    return result


@trace_function
def not_selected(num, lst):
    closest = lst[0]
    distance = abs(num - closest)
    for i in range(1, len(lst)):
        if abs(num - lst[i]) < distance:
            closest = lst[i]
            distance = abs(num - closest)
    if abs(num - closest) > 10:
        # 距离较远
        return True
    else:
        return False


@trace_function
# 检测是否有动画效果的函数,参数为等待时间
def haveAnimation(waitTime=0.1):
    # 定义需要检测动画的三个区域坐标
    regions = [
        (665, 194, 566, 175),  # 下家动画位置
        (5, 172, 584, 189),  # 上家动画位置
        (264, 329, 701, 159),  # 自己上方动画位置
    ]
    # 获取当前屏幕截图
    img = helper.Screenshot()
    # 保存当前截图作为上一帧图像
    lastImg = img
    # 循环2次检测动画
    for i in range(2):
        # 等待指定时间
        time.sleep(waitTime)
        # 再次获取屏幕截图
        img = helper.Screenshot()
        # 遍历所有需要检测的区域
        for region in regions:
            # 比较当前帧与上一帧指定区域的图像是否有变化
            if compareImage(img.crop(region), lastImg.crop(region)):
                # 如果有变化说明有动画,返回True
                return True
        # 更新上一帧图像
        lastImg = img

    # 如果没有检测到动画,返回False
    return False


@trace_function
def waitUntilNoAnimation(ms=0.1):
    ani = haveAnimation(ms)
    if ani:
        print("\n检测到炸弹、顺子、飞机 Biu~~ Biu~~  Bomb!!! Bomb!!!")
        return True
    return False


@trace_function
def animation(cards):
    move_type = get_move_type(real_to_env(cards))
    animation_types = {4, 5, 13, 14, 8, 9, 10, 11, 12}
    if move_type["type"] in animation_types or len(cards) >= 6:
        return True


class Worker(QThread):
    auto_game = pyqtSignal(int)  # Automatic start
    hand_game = pyqtSignal(int)  # Human start
    init_interface = pyqtSignal(int)  # Initialize interface
    player_display = pyqtSignal(int)  # Player Display
    state_display = pyqtSignal(str)  # 游戏状态显示
    bid_display = pyqtSignal(str)  # 叫牌score
    three_cards_display = pyqtSignal(str)  # Three cards display
    winrate_display = pyqtSignal(str)  # Winrate Display
    pre_cards_display = pyqtSignal(str)  # 显示AI推荐出牌
    left_cards_display = pyqtSignal(str)  # 显示上家的牌
    right_cards_display = pyqtSignal(str)  # 显示下家的牌
    recorder_display = pyqtSignal(str)  # 记牌器
    write_threshold = pyqtSignal(int)  # 阈值写入json
    suggest_1 = pyqtSignal(str)
    suggest_2 = pyqtSignal(str)
    init_button = pyqtSignal(int)
    warning_message = pyqtSignal(str)
    state_message = pyqtSignal(str)
    button_exchange = pyqtSignal(int)

    @trace_function
    def __init__(self):
        super(Worker, self).__init__()
        self.other_played_cards_real = None
        self.my_played_cards_real = None
        self.name = None
        self.FirstRun = None
        self.left_played_cards = None
        self.right_played_cards = None
        self.statement = None
        self.in_sign = None
        self.bid_thresholds = None
        self.auto_sign = None
        self.env = None
        self.play_order = None
        self.other_hands_cards_str = None
        self.user_hand_cards_real = None
        self.user_position = None
        self.user_position_code = None
        self.RunGame = None
        self.three_cards_env = None
        self.three_cards_real = None
        self.card_play_data_list = None
        self.other_hand_cards = None
        self.other_played_cards_env = None
        self.my_played_cards_env = None
        self.user_hand_cards_env = None

        # 所有坐标都是相对于游戏窗口左上角的坐标
        # 格式为(x, y, width, height)
        self.MyCardsPos = (54, 481, 1121, 82)  # 我的手牌区域
        self.MyPlayedPos = (292, 333, 663, 123)  # 我的出牌区域
        self.LCardsPos = (211, 239, 390, 84)  # 左边出牌区域
        self.RCardsPos = (629, 247, 411, 78)  # 右边出牌区域
        self.ThreeCardsPos = (958, 53, 139, 59)  # 地主底牌区域
        self.ButtonsPos = (214, 380, 791, 93)  # 出牌按钮区域
        self.LPassPos = (321, 253, 99, 63)  # 左边不出区域
        self.RPassPos = (825, 259, 105, 54)  # 右边不出区域
        self.MPassPos = (497, 396, 169, 69)  # 我的不出区域

        self.model_path_dict = {
            'landlord': "baselines/resnet/resnet_landlord.ckpt",
            'landlord_up': "baselines/resnet/resnet_landlord_up.ckpt",
            'landlord_down': "baselines/resnet/resnet_landlord_down.ckpt"
        }
        LandlordModel.init_model("baselines/resnet/resnet_landlord.ckpt")

    @trace_function
    def run(self):
        # 发送初始化界面信号
        self.init_interface.emit(1)
        # 初始化数据
        self.init_datas()
        # 如果是首次运行(statement=0)
        if self.statement == 0:
            # 显示免责声明信息
            self.state_message.emit("1.本助手仅供学习和技术交流使用，禁止用于任何违法、犯罪或赌博行为。\n"
                                    "2.本助手仅提供技术支持，不对用户使用中导致的任何损失或风险负责。\n"
                                    "3.用户在使用该助手时应遵循相关法律法规，并承担因违反法规而产生的全部责任。\n"
                                    "4.如果你使用了本助手，即表示您同意并接受上述免责声明的所有条款和条件。\n"
                                    "5.本助手的最终解释权归软件作者所有。")
        else:
            # 如果未检测到游戏窗口(name=0)
            if self.name == 0:
                # 显示操作提示信息
                self.warning_message.emit("请打开QQ游戏大厅-欢乐斗地主\n"
                                          "1.点击斗地主合集：\n"
                                          "2.选择经典模式\n"
                                          "3.点击软件的手动或自动按钮\n"
                                          "4.进入游戏\n")
            else:
                # 设置游戏运行标志
                self.RunGame = True
                # 如果是自动模式
                if self.auto_sign:
                    # 循环执行自动模式
                    while self.auto_sign:
                        # 游戏开始前准备
                        self.before_start()
                        # 初始化卡牌
                        self.init_cards()
                        # 等待2秒
                        time.sleep(2)
                else:
                    # 手动模式只执行一次
                    self.before_start()
                    self.init_cards()
                    time.sleep(2)
        # 发送初始化按钮信号
        self.init_button.emit(1)

    @trace_function
    def init_datas(self):
        self.FirstRun = False
        self.left_played_cards = [""]
        self.right_played_cards = [""]
        self.write_threshold.emit(1)
        time.sleep(0.1)
        self.in_sign = False
        data = read_json()
        self.bid_thresholds = [float(data['bid1']), float(data['bid2']), float(data['bid3']), float(data['bid4'])]
        self.statement = data["state"]
        if data["window"] == 0:
            self.name = 0
        else:
            self.name = 1

    @trace_function
    # 识别图像中的卡牌信息的方法
    # 参数:img-截图图像,pos-识别区域,mark-标记前缀,confidence-匹配置信度
    def cards_info(self, img, pos, mark="", confidence=0.8):
        # 初始化实际卡牌字符串
        cards_real = ""
        # 初始化大王标记
        D_king = 0
        # 初始化小王标记 
        X_king = 0
        # 遍历所有可能的卡牌
        for card in AllCards:
            # 在指定区域查找所有匹配的卡牌图像
            # result是一个列表,每个元素是一个包含(x,y,width,height)的元组,表示匹配到的图像位置和大小
            result = gh.LocateAllOnImage(img, helper.PicsCV[mark + card], region=pos, confidence=confidence)

            # 如果找到匹配的卡牌
            if len(result) > 0:
                # 过滤重复的卡牌位置,获取数量和位置列表
                count, s = cards_filter(list(result), 25)
                # 如果是大小王卡牌
                if card == "X" or card == "D":
                    # 遍历每个位置
                    for a in s:
                        # 创建颜色分类器实例
                        classifier = DC.ColorClassify(debug=True)
                        # 裁剪出卡牌区域图像
                        # img1 = img[y起点:y终点, x起点:x终点]
                        # pos[1] - y坐标起点
                        # pos[1] + pos[3] - y坐标终点(pos[3]是高度)
                        # pos[0] - x坐标起点
                        # pos[0] + pos[2] - x坐标终点(pos[2]是宽度)
                        img1 = img[pos[1]:pos[1] + pos[3], pos[0]:pos[0] + pos[2]]
                        # 进一步裁剪出王牌的颜色区域
                        # img2 = img1[y起点:y终点, x起点:x终点]
                        # a[1] - y坐标起点
                        # a[1] + a[3] - 44 - y坐标终点(a[3]是高度,减44是为了只取上半部分)
                        # a[0] - x坐标起点
                        # a[0] + 18 - x坐标终点(取18像素宽度)
                        # 减44是为了只取王牌图像的上半部分(因为颜色判断只需要上半部分)
                        # 加18是取固定宽度18像素,这个宽度刚好包含王牌的主要颜色区域
                        img2 = img1[a[1]:a[1] + a[3] - 26, a[0]:a[0] + 30]  # 注意连着裁切时img不能重名
                        # 对颜色进行分类
                        result = classifier.classify(img2)
                        # 遍历分类结果
                        for b in result:
                            # 如果是红色
                            if b[0] == "Red":
                                # 根据置信度判断是大王还是小王
                                if b[1] > 0.7:
                                    D_king = 1
                                else:
                                    X_king = 1
                # 如果是普通卡牌,将卡牌添加到结果字符串
                else:
                    cards_real += card[0] * count

        # 如果有小王,添加到结果字符串并调整顺序
        if X_king:
            cards_real += "X"
            cards_real = cards_real[-1] + cards_real[:-1]

        # 如果有大王,添加到结果字符串并调整顺序
        if D_king:
            cards_real += "D"
            cards_real = cards_real[-1] + cards_real[:-1]
        # 返回识别到的卡牌字符串
        return cards_real

    @trace_function
    def find_my_cards(self):
        img = helper.Screenshot()
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        my_cards_real = self.cards_info(img, self.MyCardsPos, mark="m")
        return my_cards_real

    @trace_function
    def find_other_cards(self, pos):
        img = helper.Screenshot()
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        other_cards_real = self.cards_info(img, pos, mark="o")
        return other_cards_real

    @trace_function
    def find_played_cards(self, pos):
        img = helper.Screenshot()
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        other_cards_real = self.cards_info(img, pos, mark="c")
        return other_cards_real

    @trace_function
    def find_three_cards(self):
        img, class_list, pos_list = yolo_info(self.ThreeCardsPos)
        if class_list is not None:
            class_list = sorted(class_list, key=lambda x: 'DX2AKQJT9876543'.index(x))
            cards = "".join(class_list)
        else:
            cards = ""
        return cards

    @trace_function
    # 点击卡牌的方法,接收要出的牌作为参数
    def click_cards(self, out_cards):
        try:
            # 获取当前手牌
            cards = self.find_my_cards()
            # 计算手牌数量
            num = len(cards)
            # 每张牌之间的间距
            space = 50
            # 在手牌区域查找左上角标记
            res1 = helper.LocateOnScreen("up_left", region=self.MyCardsPos, confidence=0.65)
            # 如果没找到标记,循环等待
            while res1 is None:
                if not self.RunGame:
                    return
                print("未找到手牌区域")
                time.sleep(0.5)
                res1 = helper.LocateOnScreen("up_left", region=self.MyCardsPos, confidence=0.65)
                self.detect_start_btn()
            # 计算起始位置
            pos = res1[0] + 5, res1[1] + 6

            # 在指定区域查找左上角标记
            res2 = helper.LocateOnScreen("up_left", region=(53, 497, 1132, 104), confidence=0.65)
            # 如果找到标记,更新起始位置
            if res2 is not None:
                # res1[0]是左上角标记的x坐标,+5是向右偏移5像素
                # res1[1]是左上角标记的y坐标,+6是向下偏移6像素
                # pos是一个元组,存储了点击牌的起始位置坐标(x,y)
                pos = res1[0] + 5, res1[1] + 6

            # 根据手牌数量生成每张牌的位置列表
            # 生成每张牌的位置列表
            # pos[0] - 起始位置的x坐标
            # pos[1] - 起始位置的y坐标
            # i - 第i张牌的索引(从0开始)
            # space - 每张牌之间的间距(50像素)
            # num - 手牌总数
            # 返回一个列表,每个元素是(x,y)坐标元组,表示每张牌的位置
            pos_list = [(int(pos[0] + i * space), pos[1]) for i in range(num)]

            # 将手牌和位置信息合并为字典
            cards_dict = defaultdict(list)
            for key, value in zip(cards, pos_list):
                cards_dict[key].append(value)
            # 转换为普通字典
            cards_dict = dict(cards_dict)
            # 创建用于记录已移除牌的字典
            remove_dict = {key: [] for key in cards_dict.keys()}
           
            # 如果要出的是王炸(大小王)
            if out_cards == "DX":
                # cards_dict["X"][0][0] - 小王牌的x坐标
                # +18 - 向右偏移18像素,确保点击在牌的中心位置
                # 578 - 固定的y坐标,表示点击的垂直位置
                helper.LeftClick2((cards_dict["X"][0][0] + 18, 578))
                # 等待0.5秒,给动画播放留出时间
                time.sleep(0.5)

            else:
               
                # 遍历要出的每张牌
                for i in out_cards:  # i - 当前要出的牌的点数
                    # 获取该点数牌的最后一个位置坐标
                    # cards_dict[i] - 该点数所有牌的位置列表
                    # [-1] - 取最后一个位置
                    # [0:2] - 取坐标的x,y值
                    cars_pos = cards_dict[i][-1][0:2]  # cars_pos - 存储(x,y)坐标的元组

                    # point参数:
                    # cars_pos[0] + 18: x坐标偏移量,使点击位置位于牌的中心
                    # cars_pos[1] + 90: y坐标偏移量,使点击位置位于牌的中心
                    point = cars_pos[0] + 18, cars_pos[1] + 90

                    # img参数:
                    # helper.Screenshot(): 获取当前屏幕截图
                    # cv2.cvtColor: 将图片从RGB格式转换为BGR格式
                    # np.asarray: 将图片转换为numpy数组
                    img = helper.Screenshot()
                    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

                   
                    # 检测当前位置的牌是什么
                    # img: 传入的屏幕截图
                    # pos: 检测区域的坐标和大小
                    #   - cars_pos[0] - 2: 检测区域左上角x坐标(当前牌的x坐标往左偏移2像素)
                    #   - 502: 检测区域左上角y坐标
                    #   - 53: 检测区域宽度
                    #   - 53: 检测区域高度
                    # mark="m": 表示检测的是中间区域的牌
                    # confidence=0.8: 图像匹配的置信度阈值,大于0.8才认为匹配成功
                    check_one = self.cards_info(img=img, pos=(cars_pos[0] - 2, 466, 64, 64), mark="m", confidence=0.8)

                    # 如果系统自动选择的牌正确且不是大小王
                    if check_one == i and check_one != "D" and check_one != "X":
                        print("腾讯自动帮你选牌：", check_one)

                    else:
                        # 点击选牌
                        helper.LeftClick2(point)
                        time.sleep(0.1)
                    # 更新移除和剩余牌的记录
                    remove_dict[i].append(cards_dict[i][-1])
                    cards_dict[i].remove(cards_dict[i][-1])
                # 截图检查选中的牌
                img = helper.Screenshot()
                img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
                # 检测选中的牌
                # img: 传入的屏幕截图
                # (160, 524, 933, 80): 检测区域的坐标和大小
                #   - 160: 检测区域左上角x坐标
                #   - 524: 检测区域左上角y坐标 
                #   - 933: 检测区域宽度
                #   - 80: 检测区域高度
                # mark="m": 表示检测的是中间区域的牌
                # 返回值: 返回检测到的所有牌的字符串
                sec_cards = self.cards_info(img, (45, 504, 1147, 101), mark="m")
                # 从手牌中移除要出的牌
                for i in out_cards:
                    cards = cards.replace(i, "", 1)
                # 如果实际选中的牌少于应该选的牌
                if len(sec_cards) < len(cards):
                    for m in sec_cards:
                        cards = cards.replace(m, "", 1)
                    # 补充点击漏掉的牌
                    # 遍历每张需要补充点击的牌
                    for n in cards:
                        # 获取牌的位置坐标(取最后一张同样的牌的x,y坐标)
                        cars_pos2 = cards_dict[n][-1][0:2]
                        # 计算实际点击位置(x坐标右移18像素,y坐标下移90像素)
                        point2 = cars_pos2[0] + 18, cars_pos2[1] + 90
                        # 在计算出的位置执行左键点击
                        helper.LeftClick2(point2)
                        # 等待0.1秒
                        time.sleep(0.1)
                        # 将点击的牌位置添加到已移除牌的记录中
                        remove_dict[n].append(cards_dict[n][-1])
                        # 从剩余牌记录中移除这张牌
                        cards_dict[n].remove(cards_dict[n][-1])
                # 如果实际选中的牌多于应该选的牌
                elif len(sec_cards) > len(cards):
                    for m in cards:
                        sec_cards = sec_cards.replace(m, "", 1)
                    # 取消多选的牌
                    for n in sec_cards:
                        cars_pos3 = remove_dict[n][0][0:2]
                        point3 = cars_pos3[0] + 18, cars_pos3[1] + 90
                        helper.LeftClick2(point3)
                        time.sleep(0.3)
                        remove_dict[n].remove(remove_dict[n][0])
        # 异常处理
        except Exception as e:
            print("检测到出牌错误")
            traceback.print_exc()
        time.sleep(0.2)

    @trace_function
    # 查找地主玩家的函数
    def find_landlord(self):
        # 获取自己的手牌
        my_cards = self.find_my_cards()
        # 如果手牌数量为20,说明自己是地主
        if len(my_cards) == 20:
            return 1
        else:
            # 获取左边玩家的出牌
            left_cards = self.find_other_cards(self.LCardsPos)
            # 获取右边玩家的出牌
            right_cards = self.find_other_cards(self.RCardsPos)
            # 如果右边玩家有出牌,说明右边是地主
            if len(right_cards) > 0:
                return 0
            # 如果左边玩家有出牌,说明左边是地主
            elif len(left_cards) > 0:
                return 2

    @trace_function
    # 检测游戏开始按钮和其他界面元素的函数
    def detect_start_btn(self):
        # 检测豆子图标,判断对局是否结束
        beans = [(363, 350, 36, 147), (363, 350, 36, 148), (363, 350, 36, 149)]
        for i in beans:
            # 在指定区域查找"over"图标
            result = helper.LocateOnScreen("over", region=i, confidence=0.9)
            # 如果找到且游戏正在进行中
            if result is not None and self.in_sign:
                print("\n豆子出现，对局结束")
                # 设置游戏结束标志
                self.RunGame = False
                self.in_sign = False
                # 尝试重置游戏环境和界面
                try:
                    # 检查游戏环境对象是否存在
                    if self.env is not None:
                        # 设置游戏结束标志
                        self.env.game_over = True
                        # 重置游戏环境
                        self.env.reset()
                    # 发送初始化界面信号
                    self.init_interface.emit(1)
                # 捕获属性错误异常
                except AttributeError as e:
                    # 打印异常堆栈信息
                    traceback.print_exc()
                # 等待3秒
                time.sleep(3)
                # 跳出循环
                break

        # 检测"继续"按钮
        result = helper.LocateOnScreen("continue", region=(544, 501, 173, 60))
        # 如果找到且游戏正在进行中
        if result is not None and self.in_sign:
            print("游戏已结束")
            self.state_display.emit("游戏已结束")
            # 设置游戏结束标志
            self.RunGame = False
            self.in_sign = False
            try:
                # 重置游戏环境
                if self.env is not None:
                    self.env.game_over = True
                    self.env.reset()
                self.init_interface.emit(1)
            except AttributeError as e:
                traceback.print_exc()
                time.sleep(1)

        # 如果开启了自动模式
        if self.auto_sign:
            # 检测并点击各种界面按钮
            # 继续按钮
            if find_pic("continue", (545, 503, 170, 60), click=True):
                time.sleep(1)
            # 奖励按钮
            if find_pic("reward", (521, 506, 199, 76), click=True):
                time.sleep(1)
            # 开始游戏按钮
            if find_pic("start_game", (201, 260, 840, 74), click=True):
                time.sleep(1)
            # 取消托管按钮
            if find_pic("tuoguan", (485, 620, 269, 92), click=True):
                time.sleep(1)
            # 确定按钮
            if find_pic("sure", (560, 405, 256, 127), click=True):
                time.sleep(1)
            # 推荐按钮
            if find_pic("tuijian", (648, 413, 194, 88), click=True):
                time.sleep(1)
            # 好的按钮
            if find_pic("good", (385, 532, 194, 78), click=True):
                time.sleep(1)
            # 知道了按钮
            if find_pic("zhidao", (527, 482, 199, 83), click=True):
                time.sleep(1)
            # 关闭按钮
            if find_pic("chacha", (920, 57, 266, 204), click=True):
                time.sleep(1)
            # 快速开始按钮
            if find_pic("quick_start", (831, 595, 219, 87), click=True):
                time.sleep(1)

    @trace_function
    # 游戏开始前的准备工作
    def before_start(self):
        # 打印开始游戏信息
        print("开始游戏")
        # 设置游戏运行标志
        self.RunGame = True
        # 设置游戏状态标志
        self.in_sign = False
        # 明牌按钮点击标志
        clicked = False
        # 循环等待直到获取到17张手牌
        while True:
            # 如果游戏结束则返回
            if not self.RunGame:
                return
            # 获取玩家手牌
            self.user_hand_cards_real = self.find_my_cards()
            # 打印手牌信息
            print(self.user_hand_cards_real)
            # 如果手牌包含"DX222"且未点击过明牌按钮
            if "DX222" in self.user_hand_cards_real:
                if not clicked:
                    # 点击明牌按钮
                    find_pic("ming_btn", self.ButtonsPos, click=True)
                    clicked = True
            # 如果获取到17张手牌则跳出循环
            if len(self.user_hand_cards_real) == 17:
                break
            # 等待0.5秒
            time.sleep(0.5)
            # 检测开始按钮
            self.detect_start_btn()
        # 打印游戏状态信息
        print("\n在游戏中")
        # 发送游戏状态信息
        self.state_display.emit("在游戏中")
        # 设置游戏状态标志
        self.in_sign = True
        # 打印手牌信息
        print("手牌：", self.user_hand_cards_real)
        # 预测叫分
        score = BidModel.predict_score(self.user_hand_cards_real)
        # 显示叫分
        self.bid_display.emit("得分：" + str(round(score, 3)))
        # 根据叫分给出建议
        if score <= self.bid_thresholds[0]:
            self.suggest_1.emit("建议： 不叫")
        else:
            self.suggest_1.emit("建议： 叫地主")

        # 根据叫分给出加倍建议
        if score <= self.bid_thresholds[2]:
            self.suggest_2.emit("建议： 不加倍")
        else:
            self.suggest_2.emit("建议： 加倍")

        # 将真实手牌转换为环境编码
        self.user_hand_cards_env = [RealCard2EnvCard[c] for c in list(self.user_hand_cards_real)]
        # 初始化其他玩家手牌列表
        self.other_hand_cards = []
        # 计算其他玩家可能持有的牌
        for i in set(AllEnvCard):
            self.other_hand_cards.extend([i] * (AllEnvCard.count(i) - self.user_hand_cards_env.count(i)))
        # 将其他玩家手牌转换为字符串
        self.other_hands_cards_str = str(''.join([EnvCard2RealCard[c] for c in self.other_hand_cards]))[::-1]
        # 显示其他玩家手牌信息
        self.recorder_display.emit(self.other_hands_cards_str)

        # 主循环
        while True:
            # 如果游戏结束则返回
            if not self.RunGame:
                return
            # 获取玩家手牌
            self.user_hand_cards_real = self.find_my_cards()
            # 如果手牌数小于17张
            if len(self.user_hand_cards_real) < 17:
                # 重置明牌按钮点击标志
                clicked = False
                # 等待直到获取到17张手牌
                while True:
                    # 如果游戏结束则返回
                    if not self.RunGame:
                        return
                    # 获取玩家手牌
                    self.user_hand_cards_real = self.find_my_cards()
                    # 打印手牌信息
                    print(self.user_hand_cards_real)
                    # 如果手牌包含"DX222"且未点击过明牌按钮
                    if "DX222" in self.user_hand_cards_real:
                        if not clicked:
                            # 点击明牌按钮
                            find_pic("ming_btn", self.ButtonsPos, click=True)
                            clicked = True
                    # 如果获取到17张手牌则跳出循环
                    if len(self.user_hand_cards_real) == 17:
                        break
                    # 等待0.5秒
                    time.sleep(0.5)
                    # 检测开始按钮
                    self.detect_start_btn()
                # 打印手牌信息
                print("手牌：", self.user_hand_cards_real)
                # 预测叫分
                score = BidModel.predict_score(self.user_hand_cards_real)
                # 显示叫分
                self.bid_display.emit("得分：" + str(round(score, 3)))
                # 根据叫分给出建议
                if score <= self.bid_thresholds[0]:
                    self.suggest_1.emit("建议： 不叫")
                else:
                    self.suggest_1.emit("建议： 叫地主")

                # 根据叫分给出加倍建议
                if score <= self.bid_thresholds[2]:
                    self.suggest_2.emit("建议： 不加倍")
                else:
                    self.suggest_2.emit("建议： 加倍")
                # 将真实手牌转换为环境编码
                self.user_hand_cards_env = [RealCard2EnvCard[c] for c in list(self.user_hand_cards_real)]
                # 初始化其他玩家手牌列表
                self.other_hand_cards = []
                # 计算其他玩家可能持有的牌
                for i in set(AllEnvCard):
                    self.other_hand_cards.extend([i] * (AllEnvCard.count(i) - self.user_hand_cards_env.count(i)))
                # 将其他玩家手牌转换为字符串
                self.other_hands_cards_str = str(''.join([EnvCard2RealCard[c] for c in self.other_hand_cards]))[::-1]
                # 显示其他玩家手牌信息
                self.recorder_display.emit(self.other_hands_cards_str)

            # 检测并处理叫地主按钮
            # 检测是否出现叫地主按钮
            if find_pic("jiao_btn", self.ButtonsPos):
                # 如果分数小于等于第一个叫分阈值
                if score <= self.bid_thresholds[0]:
                    # 如果开启了自动模式
                    if self.auto_sign:
                        # 点击不叫按钮
                        helper.ClickOnImage("bujiao", self.ButtonsPos)
                    # 发送不叫建议信号
                    self.suggest_1.emit("建议： 不叫")
                else:
                    # 如果开启了自动模式
                    if self.auto_sign:
                        # 点击叫地主按钮
                        helper.ClickOnImage("jiao_btn", self.ButtonsPos)
                    # 发送叫地主建议信号
                    self.suggest_1.emit("建议： 叫地主")

            # 检测并处理抢地主按钮
            if find_pic("qiang_btn", self.ButtonsPos):
                if score <= self.bid_thresholds[1]:
                    if self.auto_sign:
                        helper.ClickOnImage("buqiang_btn", self.ButtonsPos)
                    self.suggest_1.emit("建议： 不抢")
                else:
                    if self.auto_sign:
                        helper.ClickOnImage("qiang_btn", self.ButtonsPos)
                    self.suggest_1.emit("建议： 抢地主")

            # # 检测并处理加倍按钮
            # if find_pic("jiabei", self.ButtonsPos):
            #     # 等待1秒
            #     time.sleep(1)
            #     # 获取底牌
            #     self.three_cards_real = self.find_three_cards()
            #     # 打印底牌信息
            #     print("底牌： ", self.three_cards_real)
            #     # 显示底牌信息
            #     self.three_cards_display.emit("底牌：" + self.three_cards_real)
            #     # 获取手牌
            #     hand_cards = self.find_my_cards()
            #     # 如果是地主(20张牌)
            #     if len(hand_cards) == 20:
            #         # 使用地主模型预测分数
            #         score = LandlordModel.predict_by_model(hand_cards, self.three_cards_real)
            #         # 显示分数
            #         self.bid_display.emit("得分：" + str(round(score, 3)))
            #         # 根据分数给出加倍建议并执行
            #         if self.bid_thresholds[1] < score <= self.bid_thresholds[2]:
            #             if self.auto_sign:
            #                 helper.ClickOnImage("jiabei", self.ButtonsPos)
            #             self.suggest_2.emit("建议： 加倍")
            #         elif score > self.bid_thresholds[2]:
            #             if self.auto_sign:
            #                 helper.ClickOnImage("chaojijiabei", self.ButtonsPos)
            #             self.suggest_2.emit("建议： 超级加倍")
            #         else:
            #             if self.auto_sign:
            #                 helper.ClickOnImage("bujiabei", self.ButtonsPos, confidence=0.6)
            #             self.suggest_2.emit("建议： 不加倍")
            #         break
            #     # 如果是农民(17张牌)
            #     elif len(hand_cards) == 17:
            #         # 使用农民模型预测分数
            #         score = FarmerModel.predict(hand_cards, "up")
            #         # 显示分数
            #         self.bid_display.emit("得分：" + str(round(score, 3)))
            #         # 根据分数给出加倍建议并执行
            #         if self.bid_thresholds[1] + 0.05 < score <= self.bid_thresholds[2] + 0.05:
            #             if self.auto_sign:
            #                 helper.ClickOnImage("jiabei", self.ButtonsPos)
            #             self.suggest_2.emit("建议： 加倍")
            #         elif score > self.bid_thresholds[2] + 0.05:
            #             if self.auto_sign:
            #                 helper.ClickOnImage("chaojijiabei", self.ButtonsPos)
            #             self.suggest_2.emit("建议： 超级加倍")
            #         else:
            #             if self.auto_sign:
            #                 helper.ClickOnImage("bujiabei", self.ButtonsPos)
            #             self.suggest_2.emit("建议： 不加倍")
            #         break
            # 检测并处理明牌按钮
            if find_pic("mingpai_btn", self.ButtonsPos):
                if score > self.bid_thresholds[3]:
                    if self.auto_sign:
                        helper.ClickOnImage("mingpai_btn", self.ButtonsPos)
                time.sleep(1)
                break

            # 等待0.5秒
            time.sleep(0.5)
            # 检测开始按钮
            self.detect_start_btn()
        # 打印加倍阶段结束信息
        print("加倍阶段结束")
        # 显示加倍阶段结束信息
        self.state_display.emit("加倍阶段结束")

    @trace_function
    # 初始化卡牌相关的函数
    # 初始化卡牌相关的函数,负责识别和设置游戏中的各种卡牌信息
    def init_cards(self):
        # 打印并显示当前进入出牌前阶段的信息
        print("进入出牌前阶段")
        self.state_display.emit("出牌前阶段")
        # 设置游戏运行标志为True,表示游戏正在进行
        self.RunGame = True
        # 初始化玩家手牌的环境编码列表
        self.user_hand_cards_env = []
        # 初始化玩家已出牌的环境编码列表
        self.my_played_cards_env = []
        # 初始化其他玩家已出牌的环境编码列表
        self.other_played_cards_env = []
        # 初始化其他玩家手牌列表
        self.other_hand_cards = []
        # 初始化地主底牌的环境编码列表
        self.three_cards_env = []
        # 初始化卡牌数据字典
        self.card_play_data_list = {}
        # 开始识别底牌,直到成功识别出3张底牌
        print("正在识别底牌", end="")
        while len(self.three_cards_real) != 3:
            print(".", end="")
            # 如果游戏结束则返回
            if not self.RunGame:
                return
            # 每0.2秒尝试识别一次底牌
            time.sleep(0.2)
            self.three_cards_real = self.find_three_cards()
            self.detect_start_btn()
        # 显示识别到的底牌信息
        print("\n底牌： ", self.three_cards_real)
        self.three_cards_display.emit("底牌：" + self.three_cards_real)

        # 开始识别玩家角色,直到成功识别
        # 打印正在识别玩家角色的提示信息,end=""表示不换行
        print("正在识别玩家角色", end="")
        # 调用find_landlord()方法识别玩家角色,返回角色代码
        self.user_position_code = self.find_landlord()
        # 如果没有识别到角色代码,则循环尝试识别
        while self.user_position_code is None:
            # 如果游戏已结束则返回
            if not self.RunGame:
                return
            # 打印进度点,表示正在识别中
            print(".", end="")
            # 等待0.2秒后再次尝试
            time.sleep(0.2)
            # 再次调用find_landlord()识别玩家角色
            self.user_position_code = self.find_landlord()
            # 检测游戏开始按钮状态
            self.detect_start_btn()

        # 根据position_code设置玩家位置和角色信息
        # 根据玩家角色代码设置玩家位置(地主上家/地主/地主下家)
        self.user_position = ['landlord_up', 'landlord', 'landlord_down'][self.user_position_code]
        # 根据玩家角色代码设置中文角色名称
        user_role = ['地主上家', '地主', '地主下家'][self.user_position_code]
        # 发送玩家角色代码信号到界面显示
        self.player_display.emit(self.user_position_code)
        # 打印玩家角色信息到控制台
        print("\n我的角色：", user_role)
        # 发送玩家角色信息到界面状态栏显示
        self.state_display.emit(user_role)

        # 获取玩家手牌信息
        self.user_hand_cards_real = self.find_my_cards()
        # 如果是地主角色,需要等待直到识别到20张牌
        if self.user_position_code == 1:
            while len(self.user_hand_cards_real) != 20:
                if not self.RunGame:
                    return
                time.sleep(0.2)
                self.user_hand_cards_real = self.find_my_cards()
                self.detect_start_btn()
            self.user_hand_cards_env = [RealCard2EnvCard[c] for c in list(self.user_hand_cards_real)]
        # 如果是农民角色,需要等待直到识别到17张牌
        else:
            while len(self.user_hand_cards_real) != 17:
                if not self.RunGame:
                    return
                time.sleep(0.2)
                self.user_hand_cards_real = self.find_my_cards()
                self.detect_start_btn()
            self.user_hand_cards_env = [RealCard2EnvCard[c] for c in list(self.user_hand_cards_real)]

        # 计算其他玩家的手牌信息
        for i in set(AllEnvCard):
            self.other_hand_cards.extend([i] * (AllEnvCard.count(i) - self.user_hand_cards_env.count(i)))
        # 将其他玩家手牌转换为字符串并反转显示
        self.other_hands_cards_str = str(''.join([EnvCard2RealCard[c] for c in self.other_hand_cards]))[::-1]
        self.recorder_display.emit(self.other_hands_cards_str)
        # 更新卡牌数据字典,包含地主底牌和各玩家手牌信息
        # 更新卡牌数据字典
        self.card_play_data_list.update({
            # 添加地主底牌信息
            'three_landlord_cards': self.three_cards_env,
            # 添加当前玩家的手牌信息,根据position_code计算玩家角色
            ['landlord_up', 'landlord', 'landlord_down'][(self.user_position_code + 0) % 3]:
                self.user_hand_cards_env,
            # 添加下一个玩家的手牌信息
            # 如果下一个玩家是地主则取后17张牌,否则取前17张
            ['landlord_up', 'landlord', 'landlord_down'][(self.user_position_code + 1) % 3]:
                self.other_hand_cards[0:17] if (self.user_position_code + 1) % 3 != 1 else self.other_hand_cards[17:],
            # 添加最后一个玩家的手牌信息
            # 如果前一个玩家是地主则取前17张牌,否则取后17张
            ['landlord_up', 'landlord', 'landlord_down'][(self.user_position_code + 2) % 3]:
                self.other_hand_cards[0:17] if (self.user_position_code + 1) % 3 == 1 else self.other_hand_cards[17:]
        })
        # 根据玩家角色设置出牌顺序
        self.play_order = 0 if self.user_position == "landlord" else 1 if self.user_position == "landlord_up" else 2

        # 创建AI代理实例,设置玩家位置和对应的模型路径
        AI = [0, 0]
        AI[0] = self.user_position
        AI[1] = DeepAgent(self.user_position, self.model_path_dict[self.user_position])
        # 创建游戏环境实例
        self.env = GameEnv(AI)

        # 尝试开始游戏
        try:
            self.game_start()
        except Exception as e:
            traceback.print_exc()
            print(e)
            self.RunGame = False
            self.init_interface.emit(1)
            if self.env is not None:
                self.env.game_over = True
                self.env.reset()

    @trace_function
    # 游戏开始的主要方法
    def game_start(self):
        # 初始化游戏环境的卡牌数据
        self.env.card_play_init(self.card_play_data_list)
        # 打印游戏开始提示
        print("开始对局")
        # 发送游戏开始状态信号
        self.state_display.emit("游戏开始")
        # 初始化左右序列变量
        sequence_left = ""
        sequence_right = ""

        # 游戏主循环,直到游戏结束
        while not self.env.game_over:
            # 检查游戏是否需要继续运行
            if not self.RunGame:
                return
            # 当轮到玩家出牌时的循环
            while self.play_order == 0:
                # 再次检查游戏运行状态
                if not self.RunGame:
                    return
                # 检测玩家出的牌
                cards = self.find_played_cards(self.MyPlayedPos)
                # 如果检测到出牌,等待0.5秒后重新检测以确认
                if len(cards) > 0:
                    time.sleep(0.5)
                    cards = self.find_played_cards(self.MyPlayedPos)
                # 如果没有检测到出牌
                if len(cards) == 0:
                    # 获取AI的行动建议,但不更新状态
                    action_message, action_list = self.env.step(self.user_position, update=False)
                    # 只取前三个建议动作
                    action_list = action_list[:3]

                    # 显示当前得分
                    self.bid_display.emit("当前得分：" + str(round(float(action_list[0][1]), 3)))
                    # 显示推荐出牌
                    self.pre_cards_display.emit(action_message["action"] if action_message["action"] else "pass")
                    # 将动作列表转换为字符串并显示
                    action_list_str = " | ".join([ainfo[0] + " = " + ainfo[1] for ainfo in action_list])
                    print(action_list_str)
                    self.winrate_display.emit(action_list_str)

                    # 如果开启了自动模式
                    if self.auto_sign:
                        # 如果AI建议不出牌
                        if action_message["action"] == "":
                            # 执行不出操作
                            self.env.step(self.user_position, [])
                            # 获取剩余手牌字符串
                            hand_cards_str = ''.join(
                                [EnvCard2RealCard[c] for c in self.env.info_sets[self.user_position].player_hand_cards])
                            # 打印出牌信息
                            print("出牌:", "Pass", "| 得分:", round(action_message["win_rate"], 4), "| 剩余手牌:",
                                  hand_cards_str)

                            # 寻找不出按钮
                            # 在按钮区域查找"不出"按钮
                            pass_btn = helper.LocateOnScreen("buchu_btn", region=self.ButtonsPos, confidence=0.7)
                            # 在按钮区域查找"要不起"按钮
                            yaobuqi = helper.LocateOnScreen("yaobuqi_btn", region=self.ButtonsPos, confidence=0.7)
                            # 在玩家不出区域查找"不出"标记
                            buchu = helper.LocateOnScreen("buchu", region=self.MPassPos)
                            # 等待直到找到不出按钮
                            while pass_btn is None and yaobuqi is None and buchu is None:
                                if not self.RunGame or not self.auto_sign:
                                    return
                                pass_btn = helper.LocateOnScreen("buchu_btn", region=self.ButtonsPos, confidence=0.7)
                                yaobuqi = helper.LocateOnScreen("yaobuqi_btn", region=self.ButtonsPos, confidence=0.7)
                                buchu = helper.LocateOnScreen("buchu", region=self.MPassPos)
                                self.detect_start_btn()

                           
                            # 如果找到"不出"按钮,点击该按钮
                            if pass_btn is not None:
                                helper.ClickOnImage("buchu_btn", region=self.ButtonsPos, confidence=0.7)
                            # 如果找到"要不起"按钮,点击该按钮  
                            if yaobuqi is not None:
                                helper.ClickOnImage("yaobuqi_btn", region=self.ButtonsPos, confidence=0.7)
                            # 如果找到"不出"标记,打印提示信息并等待
                            if buchu is not None:
                                print("你们太牛X！ 我要不起")
                                time.sleep(0.5)
                            # 等待0.2秒
                            time.sleep(0.2)

                        # 如果AI建议出牌
                        else:
                            # 点击要出的牌
                            self.click_cards(action_message["action"])
                            # 寻找出牌按钮
                            play_card = helper.LocateOnScreen("play_btn", region=self.ButtonsPos, confidence=0.7)
                            # 等待直到找到出牌按钮
                            while play_card is None:
                                if not self.RunGame or not self.auto_sign:
                                    return
                                time.sleep(0.2)
                                play_card = helper.LocateOnScreen("play_btn", region=self.ButtonsPos, confidence=0.7)
                                self.detect_start_btn()

                            # 尝试点击出牌按钮
                            try:
                                helper.ClickOnImage("play_btn", region=self.ButtonsPos, confidence=0.7)
                            except Exception as e:
                                print("没找到出牌按钮")
                            print("点击出牌按钮")
                            time.sleep(0.2)
                            # 再次检查出牌按钮并重试
                            play_card = helper.LocateOnScreen("play_btn", region=self.ButtonsPos, confidence=0.7)
                            if play_card is not None:
                                self.click_cards(action_message["action"])
                                time.sleep(0.5)
                                helper.ClickOnImage("play_btn", region=self.ButtonsPos, confidence=0.7)

                            # 更新环境中的出牌信息
                            self.my_played_cards_env = [RealCard2EnvCard[c] for c in list(action_message["action"])]
                            self.my_played_cards_env.sort()
                            self.env.step(self.user_position, self.my_played_cards_env)

                            # 获取并打印剩余手牌信息
                            hand_cards_str = ''.join(
                                [EnvCard2RealCard[c] for c in self.env.info_sets[self.user_position].player_hand_cards])
                            print("出牌:", action_message["action"] if action_message["action"] else "Pass", "| 得分:",
                                  round(action_message["win_rate"], 4), "| 剩余手牌:", hand_cards_str)

                            # 处理特殊牌型的动画延迟
                            if action_message["action"] == "DX":
                                time.sleep(0.1)
                            ani = animation(action_message["action"])
                            if ani:
                                time.sleep(0.5)

                            # 如果没有剩余手牌,游戏结束
                            if len(hand_cards_str) == 0:
                                self.RunGame = False
                                try:
                                    if self.env is not None:
                                        self.env.game_over = True
                                        self.env.reset()
                                    self.init_interface.emit(1)

                                except AttributeError as e:
                                    traceback.print_exc()
                                    print("程序走到这里")
                                    time.sleep(1)
                                break

                    # 如果不是自动模式
                    if not self.auto_sign:
                        # 打印提示信息
                        print("现在是手动模式，请手动出牌")
                        # 发送按钮切换信号
                        self.button_exchange.emit(1)
                        # 播放提示音
                        play_sound("snds/1.wav")
                        # 如果AI建议不出牌
                        if action_message["action"] == "":
                            # 显示推荐pass
                            self.pre_cards_display.emit("推荐：pass")
                        else:
                            # 显示推荐出牌
                            self.pre_cards_display.emit(f"推荐：" + action_message["action"])
                        # 检测是否点击了不出按钮
                        pass_flag = helper.LocateOnScreen('buchu', region=self.MPassPos)
                        # 获取玩家出的牌
                        centralCards = self.find_played_cards(self.MyPlayedPos)
                        # 打印等待提示
                        print("等待自己出牌", end="")
                        # 当没有出牌且没有点击不出时循环等待
                        while len(centralCards) == 0 and pass_flag is None:
                            # 如果游戏结束或切换到自动模式则返回
                            if not self.RunGame or self.auto_sign or self.env.game_over:
                                return
                            # 打印等待点
                            print(".", end="")
                            # 等待0.2秒
                            time.sleep(0.2)
                            # 检查是否有动画播放
                            have_ani = waitUntilNoAnimation()
                            # 如果有动画播放
                            if have_ani:
                                # 显示等待动画提示
                                self.pre_cards_display.emit("等待动画")
                                # 等待动画播放
                                time.sleep(0.2)
                            # 再次检测不出按钮
                            pass_flag = helper.LocateOnScreen('buchu', region=self.MPassPos)
                            # 再次获取出牌
                            centralCards = self.find_played_cards(self.MyPlayedPos)
                            # 检测开始按钮
                            self.detect_start_btn()

                        # 如果没有点击不出按钮
                        if pass_flag is None:
                            # 循环检测直到确认出牌
                            while True:
                                # 如果游戏结束或切换到自动模式则返回
                                if not self.RunGame or self.auto_sign:
                                    return
                                # 第一次获取出牌区域的牌
                                centralOne = self.find_played_cards(self.MyPlayedPos)
                                # 等待0.3秒
                                time.sleep(0.3)
                                # 第二次获取出牌区域的牌
                                centralTwo = self.find_played_cards(self.MyPlayedPos)
                                # 如果两次获取的牌相同且不为空,说明出牌已经稳定
                                if centralOne == centralTwo and len(centralOne) > 0:
                                    # 记录实际出的牌
                                    self.my_played_cards_real = centralOne
                                    # 如果出的牌中包含大小王(但不是王炸)
                                    if ("X" in centralOne or "D" in centralOne) and not ("DX" in centralOne):
                                        # 额外等待0.5秒
                                        time.sleep(0.5)
                                        # 再次获取出牌区域的牌
                                        self.my_played_cards_real = self.find_played_cards(self.MyPlayedPos)
                                        # 如果没有检测到牌,使用之前记录的牌
                                        if len(self.my_played_cards_real) == 0:
                                            self.my_played_cards_real = centralOne
                                    # 跳出循环
                                    break
                                # 检测开始按钮
                                self.detect_start_btn()
                        # 如果点击了不出按钮
                        else:
                            # 记录为不出
                            self.my_played_cards_real = ""
                        # 打印出牌信息
                        print("\n自己出牌：", self.my_played_cards_real if self.my_played_cards_real else "pass")
                        # 显示出牌信息
                        self.pre_cards_display.emit(self.my_played_cards_real if self.my_played_cards_real else "pass")
                        # 将实际出的牌转换为环境中的牌
                        self.my_played_cards_env = [RealCard2EnvCard[c] for c in list(self.my_played_cards_real)]
                        # 对转换后的牌进行排序
                        self.my_played_cards_env.sort()
                        # 在环境中执行出牌动作
                        action_message, _ = self.env.step(self.user_position, self.my_played_cards_env)
                        # 获取剩余手牌字符串
                        hand_cards_str = ''.join(
                            [EnvCard2RealCard[c] for c in self.env.info_sets[self.user_position].player_hand_cards])

                        # 打印出牌结果信息
                        print("出牌:", action_message["action"] if action_message["action"] else "Pass", "| 得分:",
                              round(action_message["win_rate"], 4), "| 剩余手牌:", hand_cards_str)

                    # 等待0.5秒
                    time.sleep(0.5)
                    # 设置出牌顺序为1(下家)
                    self.play_order = 1
                # 如果已经出过牌
                else:
                    # 打印提示信息
                    print("已经出过牌")
                    # 等待0.5秒
                    time.sleep(0.5)
                    # 设置出牌顺序为1(下家)
                    self.play_order = 1
                # 检测开始按钮
                self.detect_start_btn()
            # 检测开始按钮
            self.detect_start_btn()

            # 如果轮到下家出牌
            if self.play_order == 1:
                # 显示下家出牌序列
                self.right_cards_display.emit(sequence_right)

                # 检测下家是否点击不出按钮
                pass_flag = helper.LocateOnScreen('buchu', region=self.RPassPos)
                # 获取下家出的牌
                rightCards = self.find_other_cards(self.RCardsPos)
                # 打印等待提示
                print("等待下家出牌", end="")

                # 当没有出牌且没有点击不出时循环等待
                while len(rightCards) == 0 and pass_flag is None:
                    # 如果游戏结束则返回
                    if not self.RunGame:
                        return
                    # 打印等待点
                    print(".", end="")
                    # 等待0.2秒
                    time.sleep(0.2)
                    # 检查是否有动画播放
                    have_ani = waitUntilNoAnimation()
                    # 如果有动画播放则等待
                    if have_ani:
                        time.sleep(0.2)
                    # 再次检测不出按钮
                    pass_flag = helper.LocateOnScreen('buchu', region=self.RPassPos)
                    # 再次获取出牌
                    rightCards = self.find_other_cards(self.RCardsPos)
                    # 检测开始按钮
                    self.detect_start_btn()

                # 如果没有点击不出按钮
                if pass_flag is None:
                    # 循环检测直到确认出牌
                    while True:
                        # 如果游戏结束则返回
                        if not self.RunGame:
                            return
                        # 第一次获取下家出牌区域的牌
                        rightOne = self.find_other_cards(self.RCardsPos)
                        # 等待0.3秒
                        time.sleep(0.3)
                        # 第二次获取下家出牌区域的牌
                        rightTwo = self.find_other_cards(self.RCardsPos)

                        # 如果两次获取的牌相同且不为空,说明出牌已经稳定
                        if rightOne == rightTwo and len(rightOne) > 0:
                            # 记录下家实际出的牌
                            self.other_played_cards_real = rightOne
                            # 如果出的牌中包含大小王(但不是王炸)
                            if "X" in rightOne or "D" in rightOne and not ("DX" in rightOne):
                                # 额外等待0.5秒
                                time.sleep(0.5)
                                # 再次获取下家出牌区域的牌
                                self.other_played_cards_real = self.find_other_cards(self.RCardsPos)
                                # 如果没有检测到牌,使用之前记录的牌
                                if len(self.other_played_cards_real) == 0:
                                    self.other_played_cards_real = rightOne
                            # 更新下家出牌序列
                            sequence_right = self.other_played_cards_real + "-" + sequence_right
                            # 显示更新后的下家出牌序列
                            self.right_cards_display.emit(sequence_right)
                            # 跳出循环
                            break
                        # 如果两次获取的牌不同或为空
                        else:
                            # 检测不出按钮
                            pass_flag = helper.LocateOnScreen('buchu', region=self.RPassPos)
                            # 如果点击了不出按钮
                            if pass_flag is not None:
                                # 记录为不出
                                self.other_played_cards_real = ""
                                # 更新下家出牌序列为不出
                                self.right_cards_display.emit("pass" + "-" + sequence_right)
                                # 跳出循环
                                break
                        # 检测开始按钮
                        self.detect_start_btn()
                # 如果点击了不出按钮
                else:
                    # 记录为不出
                    self.other_played_cards_real = ""
                    # 更新下家出牌序列为不出
                    self.right_cards_display.emit("pass" + "-" + sequence_right)
                # 打印下家出牌信息
                print("\n下家出牌：", self.other_played_cards_real if self.other_played_cards_real else "pass")
                # 将下家实际出的牌转换为环境中的牌
                self.other_played_cards_env = [RealCard2EnvCard[c] for c in list(self.other_played_cards_real)]
                # 对转换后的牌进行排序
                self.other_played_cards_env.sort()
                # 在环境中执行下家出牌动作
                self.env.step(self.user_position, self.other_played_cards_env)
                # 更新下家剩余手牌
                self.other_hands_cards_str = subtract_strings(self.other_hands_cards_str, self.other_played_cards_real)
                # 显示更新后的下家手牌
                self.recorder_display.emit(self.other_hands_cards_str)
                # 等待0.2秒
                time.sleep(0.2)
                # 设置出牌顺序为2(上家)
                self.play_order = 2

            # 如果轮到上家出牌
            if self.play_order == 2:
                # 显示上家出牌序列
                self.left_cards_display.emit(sequence_left)

                # 检测上家是否点击不出按钮
                pass_flag = helper.LocateOnScreen('buchu', region=self.LPassPos)
                # 获取上家出的牌
                leftCards = self.find_other_cards(self.LCardsPos)
                # 打印等待提示
                print("等待上家出牌", end="")
                # 当没有出牌且没有点击不出时循环等待
                while len(leftCards) == 0 and pass_flag is None:
                    # 如果游戏结束则返回
                    if not self.RunGame:
                        return
                    # 打印等待点
                    print(".", end="")
                    # 等待0.2秒
                    time.sleep(0.2)
                    # 检查是否有动画播放
                    have_ani = waitUntilNoAnimation()
                    # 如果有动画播放则等待
                    if have_ani:
                        time.sleep(0.2)
                    # 再次检测不出按钮
                    pass_flag = helper.LocateOnScreen('buchu', region=self.LPassPos)
                    # 再次获取出牌
                    leftCards = self.find_other_cards(self.LCardsPos)
                    # 检测开始按钮
                    self.detect_start_btn()

                # 如果没有点击不出按钮
                if pass_flag is None:
                    # 循环检测直到确认出牌
                    while True:
                        # 如果游戏结束则返回
                        if not self.RunGame:
                            return
                        # 第一次获取上家出牌区域的牌
                        leftOne = self.find_other_cards(self.LCardsPos)
                        # 等待0.3秒
                        time.sleep(0.3)
                        # 第二次获取上家出牌区域的牌
                        leftTwo = self.find_other_cards(self.LCardsPos)
                        # 如果两次获取的牌相同且不为空,说明出牌已经稳定
                        if leftOne == leftTwo and len(leftOne) > 0:
                            # 记录上家实际出的牌
                            self.other_played_cards_real = leftOne
                            # 如果出的牌中包含大小王(但不是王炸)
                            if ("X" in leftOne or "D" in leftOne) and not ("DX" in leftOne):
                                # 额外等待0.5秒
                                time.sleep(0.5)
                                # 再次获取上家出牌区域的牌
                                self.other_played_cards_real = self.find_other_cards(self.LCardsPos)
                                # 如果没有检测到牌,使用之前记录的牌
                                if len(self.other_played_cards_real) == 0:
                                    self.other_played_cards_real = leftOne
                            # 更新上家出牌序列
                            sequence_left = self.other_played_cards_real + "-" + sequence_left
                            # 显示更新后的上家出牌序列
                            self.left_cards_display.emit(sequence_left)
                            # 跳出循环
                            break
                        # 如果两次获取的牌不同或为空
                        else:
                            # 检测不出按钮
                            pass_flag = helper.LocateOnScreen('buchu', region=self.LPassPos)
                            # 如果点击了不出按钮
                            if pass_flag is not None:
                                # 记录为不出
                                self.other_played_cards_real = ""
                                # 更新上家出牌序列为不出
                                self.left_cards_display.emit("pass" + "-" + sequence_left)
                                # 跳出循环
                                break
                        # 检测开始按钮
                        self.detect_start_btn()
                # 如果点击了不出按钮
                else:
                    # 记录为不出
                    self.other_played_cards_real = ""
                    # 更新上家出牌序列为不出
                    self.left_cards_display.emit("pass" + "-" + sequence_left)

                # 打印上家出牌信息
                print("\n上家出牌：", self.other_played_cards_real if self.other_played_cards_real else "pass")
                # 将上家实际出的牌转换为环境中的牌
                self.other_played_cards_env = [RealCard2EnvCard[c] for c in list(self.other_played_cards_real)]
                # 对转换后的牌进行排序
                self.other_played_cards_env.sort()
                # 在环境中执行上家出牌动作
                self.env.step(self.user_position, self.other_played_cards_env)
                # 更新上家剩余手牌
                self.other_hands_cards_str = subtract_strings(self.other_hands_cards_str,
                                                              self.other_played_cards_real)
                # 显示更新后的上家手牌
                self.recorder_display.emit(self.other_hands_cards_str)
                # 等待0.05秒
                time.sleep(0.05)
                # 设置出牌顺序为0(自己)
                self.play_order = 0

        # 打印游戏结束提示
        print("游戏结束")
        # 设置游戏运行标志为False
        self.RunGame = False
        # 设置进入标志为False
        self.in_sign = False
        # 显示游戏结束状态
        self.state_display.emit("游戏结束")
        # 初始化界面
        self.init_interface.emit(1)
        # 等待2秒
        time.sleep(2)


class MaYun(QtWidgets.QWidget, Ui_Form):
    @trace_function
    def __init__(self):
        super(MaYun, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint |  # 使能最小化按钮
                            QtCore.Qt.WindowStaysOnTopHint |  # 窗体总在最前端
                            QtCore.Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(':/pics/favicon.ico'))
        self.setWindowTitle("欢乐斗地主5.8（QQ游戏大厅版）")
        self.setFixedSize(self.width(), self.height())  # 固定窗体大小
        self.move(20, 20)
        window_pale = QtGui.QPalette()
        self.setPalette(window_pale)
        self.setWindowOpacity(1)

        self.HandButton.clicked.connect(self.hand_game)
        self.AutoButton.clicked.connect(self.auto_game)
        self.StopButton.clicked.connect(self.stop)
        self.ResetButton.clicked.connect(self.init_threshold)

        self.Players = [self.RPlayedCard, self.PredictedCard, self.LPlayedCard]
        self.thread = Worker()
        self.init_info()
        self.thread.auto_game.connect(self.auto_game)
        self.thread.hand_game.connect(self.hand_game)
        self.thread.init_interface.connect(self.init_interface)
        self.thread.player_display.connect(self.player_display)
        self.thread.state_display.connect(self.state_display)
        self.thread.three_cards_display.connect(self.three_cards_display)
        self.thread.bid_display.connect(self.bid_display)
        self.thread.winrate_display.connect(self.winrate_display)
        self.thread.pre_cards_display.connect(self.pre_cards_display)
        self.thread.left_cards_display.connect(self.left_cards_display)
        self.thread.right_cards_display.connect(self.right_cards_display)
        self.thread.recorder_display.connect(self.cards_recorder)
        self.thread.write_threshold.connect(self.write_threshold)
        self.thread.suggest_1.connect(self.suggest1_text)
        self.thread.suggest_2.connect(self.suggest2_text)
        self.thread.init_button.connect(self.init_button)
        self.thread.warning_message.connect(self.warning_message)
        self.thread.state_message.connect(self.state_message)
        self.thread.button_exchange.connect(self.button_exchange)

    @trace_function
    def hand_game(self, result):
        self.thread.auto_sign = False
        self.thread.start()
        GameHelper()
        self.AutoButton.setStyleSheet('background-color: none;')
        self.HandButton.setStyleSheet('background-color: rgba(255, 85, 255, 0.5);')

    @trace_function
    def auto_game(self, result):
        self.thread.auto_sign = True
        self.thread.start()
        GameHelper()
        self.AutoButton.setStyleSheet('background-color: rgba(255, 85, 255, 0.5);')
        self.HandButton.setStyleSheet('background-color: none;')

    @trace_function
    def button_exchange(self):
        self.AutoButton.setStyleSheet('background-color: none;')
        self.HandButton.setStyleSheet('background-color: rgba(255, 85, 255, 0.5);')

    @trace_function
    def stop(self, result):
        print()
        print("停止线程")
        self.thread.terminate()
        self.init_interface(1)
        self.AutoButton.setStyleSheet('background-color: none;')
        self.HandButton.setStyleSheet('background-color: none;')

    @trace_function
    def init_button(self, result):
        self.AutoButton.setStyleSheet('background-color: none;')
        self.HandButton.setStyleSheet('background-color: none;')

    @trace_function
    def player_display(self, result):
        for player in self.Players:
            player.setStyleSheet('background-color: rgba(0, 255, 0, 0);')
        self.Players[result].setStyleSheet('background-color: rgba(0, 255, 0, 0.5);')

    @trace_function
    def init_threshold(self):
        self.bid_lineEdit_1.setText("0.6")
        self.bid_lineEdit_2.setText("0.7")
        self.bid_lineEdit_3.setText("0.8")
        self.bid_lineEdit_4.setText("0.95")
        self.write_threshold(1)

    @trace_function
    def write_threshold(self, result):
        data = read_json()
        data['bid1'] = self.bid_lineEdit_1.text()
        data['bid2'] = self.bid_lineEdit_2.text()
        data['bid3'] = self.bid_lineEdit_3.text()
        data['bid4'] = self.bid_lineEdit_4.text()
        write_json(data)

    @trace_function
    def init_info(self):
        GameHelper()
        data = read_json()
        self.bid_lineEdit_1.setText(data['bid1'])
        self.bid_lineEdit_2.setText(data['bid2'])
        self.bid_lineEdit_3.setText(data['bid3'])
        self.bid_lineEdit_4.setText(data['bid4'])

    @trace_function
    def init_interface(self, result):
        self.WinRate.setText("评分")
        self.WinRate.setStyleSheet('background-color: none;')
        self.label.setText("游戏状态")
        self.BidWinrate.setText("得分")
        self.label.setStyleSheet('background-color: none;')
        self.LPlayedCard.setText("上家出牌区域")
        self.RPlayedCard.setText("下家出牌区域")
        self.PredictedCard.setText("AI出牌区域")
        self.ThreeLandlordCards.setText("底牌")
        self.suggest_1.setText("建议")
        self.suggest_2.setText("建议")
        self.recorder2zero()
        for player in self.Players:
            player.setStyleSheet('background-color: none;')

    @trace_function
    def state_display(self, result):
        self.label.setText(result)
        self.label.setStyleSheet('background-color: rgba(0, 0, 255, 0.5);')

    @trace_function
    def suggest1_text(self, result):
        self.suggest_1.setText(result)

    @trace_function
    def suggest2_text(self, result):
        self.suggest_2.setText(result)

    @trace_function
    def three_cards_display(self, result):
        self.ThreeLandlordCards.setText(result)

    @trace_function
    def bid_display(self, result):
        self.BidWinrate.setText(result)

    @trace_function
    def pre_cards_display(self, result):
        self.PredictedCard.setText(result)
        self.PredictedCard.setStyleSheet('background-color: rgba(0, 255, 0, 0.5);')
        self.LPlayedCard.setStyleSheet('background-color: rgba(0, 255, 0, 0);')
        self.RPlayedCard.setStyleSheet('background-color: rgba(0, 255, 0, 0);')

    @trace_function
    def left_cards_display(self, result):
        self.LPlayedCard.setText(result)
        self.PredictedCard.setStyleSheet('background-color: rgba(0, 255, 0, 0);')
        self.LPlayedCard.setStyleSheet('background-color: rgba(0, 255, 0, 0.5);')
        self.RPlayedCard.setStyleSheet('background-color: rgba(0, 255, 0, 0);')

    @trace_function
    def right_cards_display(self, result):
        self.RPlayedCard.setText(result)
        self.PredictedCard.setStyleSheet('background-color: rgba(0, 255, 0, 0);')
        self.LPlayedCard.setStyleSheet('background-color: rgba(0, 255, 0, 0);')
        self.RPlayedCard.setStyleSheet('background-color: rgba(0, 255, 0, 0.5);')

    @trace_function
    def winrate_display(self, result):
        self.WinRate.setText(result)
        self.WinRate.setStyleSheet('background-color: rgba(255, 85, 0, 0.4);')

    @trace_function
    def cards_recorder(self, result):
        for i in range(15):
            char = AllCards[i]
            num = result.count(char)
            newItem = QTableWidgetItem(str(num))
            if num == 4:
                newItem.setForeground(QColor("red"))
            newItem.setTextAlignment(Qt.AlignHCenter)
            self.tableWidget.setItem(0, i, newItem)

    @trace_function
    def recorder2zero(self):
        for i in range(15):
            newItem = QTableWidgetItem("0")
            newItem.setTextAlignment(Qt.AlignHCenter)
            self.tableWidget.setItem(0, i, newItem)

    @trace_function
    def warning_message(self, result):
        QMessageBox.about(self, "温馨提示", result)

    @trace_function
    def state_message(self, result):
        reply = QMessageBox.information(self, '免责声明', result, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            data = read_json()
            data["state"] = 1
            write_json(data)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MaYun()
    main.show()
    sys.exit(app.exec_())
