# -*- coding: utf-8 -*-
# @Time : 2024/2/14 17:06
# @Author : MaYun
# @File : GameHelper.py
# @Software: PyCharm
import ctypes
import json
import win32gui
import win32ui
import win32api
import win32con
from ctypes import windll
from PIL import Image
import cv2
import pyautogui
import pygame
import numpy as np
import requests
import os
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime, QEventLoop
from log_utils import trace_function

Pics = {}

@trace_function
def read_json():
    with open('weights/data.json', 'r') as f:
        content = f.read()
        data = json.loads(content)
        f.close()
    return data

@trace_function
def write_json(data):
    with open('weights/data.json', 'w') as f:
        json.dump(data, f)
        f.close()

@trace_function
def subtract_strings(str1, str2):
    for char1, char2 in zip(str1, str2):
        # 如果字符2在字符1中出现，则从字符1中删除该字符
        if char2 in str1:
            str1 = str1.replace(char2, '', 1)
    result = str1
    return result

@trace_function
def DrawRectWithText(image, rect, text):
    img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    x, y, w, h = rect
    img2 = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    img2 = cv2.putText(img2, text, (x, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    return Image.fromarray(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))

@trace_function
def CompareCard(card):
    order = {"3": 0, "4": 1, "5": 2, "6": 3, "7": 4, "8": 5, "9": 6, "T": 7, "J": 8, "Q": 9, "K": 10, "A": 11, "2": 12,
             "X": 13, "D": 14}
    return order[card]

@trace_function
def CompareCardInfo(card):
    order = {"3": 0, "4": 1, "5": 2, "6": 3, "7": 4, "8": 5, "9": 6, "T": 7, "J": 8, "Q": 9, "K": 10, "A": 11, "2": 12,
             "X": 13, "D": 14}
    return order[card[0]]

@trace_function
def CompareCards(cards1, cards2):
    if len(cards1) != len(cards2):
        return False
    cards1.sort(key=CompareCard)
    cards2.sort(key=CompareCard)
    for i in range(0, len(cards1)):
        if cards1[i] != cards2[i]:
            return False
    return True

@trace_function
def GetListDifference(l1, l2):
    temp1 = []
    temp1.extend(l1)
    temp2 = []
    temp2.extend(l2)
    for i in l2:
        if i in temp1:
            temp1.remove(i)
    for i in l1:
        if i in temp2:
            temp2.remove(i)
    return temp1, temp2

@trace_function
def FindImage(fromImage, template, threshold=0.8):
    w, h, _ = template.shape
    fromImage = cv2.cvtColor(np.asarray(fromImage), cv2.COLOR_RGB2BGR)
    res = cv2.matchTemplate(fromImage, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    points = []
    for pt in zip(*loc[::-1]):
        points.append(pt)
    return points

@trace_function
# 在图像中定位模板图像的位置
# 参数:
# image: 要搜索的大图像
# template: 要查找的模板图像
# region: 搜索区域,格式为(x,y,w,h),默认为None表示搜索整个图像
# confidence: 匹配置信度阈值,默认0.8
def LocateOnImage(image, template, region=None, confidence=0.8):
    # 如果指定了搜索区域,则裁剪图像
    if region is not None:
        x, y, w, h = region
        image = image[y:y + h, x:x + w, :]
    # 使用模板匹配方法在图像中查找模板
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    # 获取最佳匹配位置
    _, _, _, maxLoc = cv2.minMaxLoc(res)
    # 如果匹配度超过阈值,返回匹配位置坐标
    if (res >= confidence).any():
        return region[0] + maxLoc[0], region[1] + maxLoc[1]
    # 否则返回None表示未找到匹配
    else:
        return None

@trace_function
# 在图像中定位所有匹配模板的位置
# 参数:
# image: 要搜索的大图像
# template: 要查找的模板图像
# region: 搜索区域,格式为(x,y,w,h),默认为None表示搜索整个图像
# confidence: 匹配置信度阈值,默认0.8
def LocateAllOnImage(image, template, region=None, confidence=0.8):
    # 如果指定了搜索区域,则裁剪图像
    if region is not None:
        x, y, w, h = region
        image = image[y:y + h, x:x + w]
    # 获取图像的宽度和高度
    w, h = image.shape[1], image.shape[0]

    # 使用模板匹配方法在图像中查找所有匹配位置
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    # 获取所有匹配度超过阈值的位置
    loc = np.where(res >= confidence)
    # 存储所有匹配位置的列表
    points = []
    # 将匹配位置添加到列表中
    for pt in zip(*loc[::-1]):
        points.append((pt[0], pt[1], w, h))
    # 返回所有匹配位置
    return points

@trace_function
def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

class GameHelper:
    @trace_function
    def __init__(self):
        self.ScreenZoomRate = None
        self.counter = QTime()
        self.Pics = {}
        self.PicsCV = {}
        data = read_json()
        # 句柄(Handle)是Windows系统中用来标识和操作窗口的唯一ID号
        # 要测试是否能正确获取雷电模拟器窗口,可以:
        # 1. 先用 win32gui.FindWindow() 获取句柄
        # 2. 打印句柄值看是否为0(为0表示未找到窗口)
        # 3. 可以用 win32gui.GetWindowText(句柄) 获取窗口标题验证
        self.Handle = win32gui.FindWindow("LDPlayerMainFrame", None)
        # 添加以下代码进行测试:
        if self.Handle == 0:
            print("未找到雷电模拟器窗口!")
        else:
            print(f"成功获取雷电模拟器窗口句柄: {self.Handle}")
            print(f"窗口标题: {win32gui.GetWindowText(self.Handle)}")
        if self.Handle == 0:
            data["window"] = 0
        else:
            data["window"] = 1
        write_json(data)
        self.Interrupt = False
        self.RealRate = (1280, 720)
        self.GetZoomRate()
        for file in os.listdir("./pics"):
            info = file.split(".")
            if info[1] == "png":
                tmpImage = Image.open("./pics/" + file)
                imgCv = cv2.imread("./pics/" + file)
                self.Pics.update({info[0]: tmpImage})
                self.PicsCV.update({info[0]: imgCv})

    @trace_function
    def sleep(self, ms):
        self.counter.restart()
        while self.counter.elapsed() < ms:
            QtWidgets.QApplication.processEvents(QEventLoop.AllEvents, 50)

    @trace_function
    def Screenshot(self, region=None):  # -> (im, (left, top))
        try_count = 3
        success = False
        hwnd = self.Handle
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        # 调整窗口大小
        # hwnd: 窗口句柄,用于标识要移动的窗口
        # left和top: 保持窗口原来的位置不变,这里使用GetWindowRect获取的left和top值
        #           这样可以在调整窗口大小时不改变窗口在屏幕上的位置
        # 1280: 窗口的新宽度(像素)
        # 720: 窗口的新高度(像素)
        # True: 是否重绘窗口(True表示重绘)
        win32gui.MoveWindow(hwnd, left, top, 1280, 720, True)
        width = 1280
        height = 720
        self.RealRate = (width, height)
        while try_count > 0 and not success:
            try:
                try_count -= 1
                hwndDC = win32gui.GetWindowDC(hwnd)
                mfcDC = win32ui.CreateDCFromHandle(hwndDC)
                saveDC = mfcDC.CreateCompatibleDC()
                saveBitMap = win32ui.CreateBitmap()
                saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
                saveDC.SelectObject(saveBitMap)
                result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
                bmpinfo = saveBitMap.GetInfo()
                bmpstr = saveBitMap.GetBitmapBits(True)
                im = Image.frombuffer(
                    "RGB",
                    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                    bmpstr, 'raw', 'BGRX', 0, 1)
                win32gui.DeleteObject(saveBitMap.GetHandle())
                saveDC.DeleteDC()
                mfcDC.DeleteDC()
                win32gui.ReleaseDC(hwnd, hwndDC)
                im = im.resize((1280, 720))
                if region is not None:
                    im = im.crop((region[0], region[1], region[0] + region[2], region[1] + region[3]))
                if result:
                    success = True
                    return im
            except Exception as e:
                print("截图时出现错误:", repr(e))
                self.sleep(200)
        return None

    @trace_function
    def GetZoomRate(self):
        self.ScreenZoomRate = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

    @trace_function
    def LocateOnScreen(self, templateName, region, confidence=0.8, img=None):
        if img is not None:
            image = img
        else:
            image = self.Screenshot()
        imgcv = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        return LocateOnImage(imgcv, self.PicsCV[templateName], region=region, confidence=confidence)

    @trace_function
    # 在图像上点击指定模板位置的方法
    def ClickOnImage(self, templateName, region=None, confidence=0.8, img=None):
        # 如果提供了图像参数,使用该图像
        if img is not None:
            image = img
        # 否则截取当前屏幕
        else:
            image = self.Screenshot()
        # 将图像从RGB格式转换为BGR格式
        imgcv = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        # 在图像中定位指定的模板
        result = LocateOnImage(imgcv, self.PicsCV[templateName], region=region, confidence=confidence)

        # 如果找到了模板位置,在该位置执行点击
        if result is not None:
            self.LeftClick(result)
            # print(result)

    @trace_function
    def LeftClick(self, pos):
        """
        在指定位置执行鼠标左键点击
        - 将游戏内坐标(1280x720)转换为实际窗口坐标
        - 获取窗口位置并计算绝对坐标
        - 发送鼠标点击消息
        - 点击后将鼠标移到固定位置
        """
        # 将相对坐标转换为实际窗口坐标
        x = int((pos[0] / 1280) * self.RealRate[0])
        y = int((pos[1] / 720) * self.RealRate[1])

        # 获取窗口左上角坐标
        left, top, _, _ = win32gui.GetWindowRect(self.Handle)
        # 计算鼠标点击的绝对坐标
        m, n = int(left + x), int(top + y)
        # 保存客户区相对坐标
        client_pos = (x, y)
        # 设置鼠标位置
        win32api.SetCursorPos((m, n))
        # 将坐标打包成LONG类型
        tmp = win32api.MAKELONG(client_pos[0], client_pos[1])

        # 激活目标窗口
        win32gui.PostMessage(self.Handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        # 发送鼠标左键按下消息
        win32gui.SendMessage(self.Handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp)
        # 发送鼠标左键抬起消息
        win32gui.SendMessage(self.Handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)
        # 等待200毫秒
        self.sleep(200)
        # 将鼠标移动到指定位置
        win32api.SetCursorPos((int(left + 1000), int(top + 550)))

    @trace_function
    def LeftClick2(self, pos):
        """
        在指定位置执行鼠标左键点击的另一个版本
        与LeftClick基本相同,但点击后不移动鼠标位置
        """
        # 将相对坐标转换为实际窗口坐标
        x = int((pos[0] / 1280) * self.RealRate[0])
        y = int((pos[1] / 720) * self.RealRate[1])

        # 获取窗口左上角坐标
        left, top, _, _ = win32gui.GetWindowRect(self.Handle)
        # 计算鼠标点击的绝对坐标
        m, n = int(left + x), int(top + y)
        # 保存客户区相对坐标
        client_pos = (x, y)

        # 设置鼠标位置
        win32api.SetCursorPos((m, n))
        # 将坐标打包成LONG类型
        tmp = win32api.MAKELONG(client_pos[0], client_pos[1])
        # 激活目标窗口
        win32gui.PostMessage(self.Handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        # 发送鼠标左键按下消息
        win32gui.SendMessage(self.Handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp)
        # 发送鼠标左键抬起消息
        win32gui.SendMessage(self.Handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)

    @trace_function
    def MoveTo(self, pos):
        """
        将鼠标移动到指定位置
        - 将游戏内坐标转换为实际窗口坐标
        - 使用pyautogui移动鼠标
        """
        x = int((pos[0] / 1280) * self.RealRate[0])
        y = int((pos[1] / 720) * self.RealRate[1])
        left, top, _, _ = win32gui.GetWindowRect(self.Handle)
        x, y = int(left + x), int(top + y)
        pyautogui.moveTo(x, y)

    @trace_function
    @staticmethod
    def MouseScroll(amount):
        """
        执行鼠标滚轮滚动
        amount: 滚动的数量,正数向上滚动,负数向下滚动
        """
        # 发送鼠标滚轮事件
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, amount, 0)
