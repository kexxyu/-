# 导入numpy用于数值计算
import numpy as np
# 导入OpenCV库用于图像处理
import cv2
# 导入os库用于文件路径操作
import os

# 设置最小置信度阈值
min_confidence = 0.3
# 设置非极大值抑制阈值,数值越小精度越高
nm_threshold = 0.1  
# 设置权重文件路径
weightsPath = os.path.sep.join(['weights', "cards.weights"])
# 设置配置文件路径
configPath = os.path.sep.join(['weights', "cards.cfg"])
# 定义标签列表,包含所有扑克牌面值
LABELS = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', 'X', 'D']

# 为每个标签随机生成RGB颜色值
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
# 从配置文件和权重文件加载YOLO神经网络
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)


# 定义YOLO目标检测函数
def yolo_detect(image):  # 0 检测所有,1:只检查牌,2:检查状态
    # 初始化结果列表
    class_list = []
    cen_list = []
    c_list = []
    pos_list = []
    # 获取图像尺寸
    (H, W) = image.shape[:2]

    # 获取网络层名称
    ln = net.getLayerNames()

    # 获取输出层索引
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
    # 预处理图像,转换为blob格式
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    # 设置网络输入
    net.setInput(blob)
    # 前向传播获取检测结果
    layerOutputs = net.forward(ln)
    # 初始化检测框、位置、置信度和类别ID列表
    boxes = []
    positions = []
    confidences = []
    classIDs = []

    # 遍历每个输出层
    for output in layerOutputs:
        # 遍历每个检测结果
        for detection in output:
            # 获取类别概率
            scores = detection[5:]
            # 获取最高概率的类别ID
            classID = np.argmax(scores)
            # 获取置信度
            confidence = scores[classID]

            # 如果置信度超过阈值则保存检测结果
            if confidence > min_confidence:
                # 计算边界框坐标
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # 保存检测框信息
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # 执行非极大值抑制
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, nm_threshold)

    # 如果有检测到的对象
    if len(idxs) > 0:
        # 遍历每个检测结果
        for i in idxs.flatten():
            # 获取边界框坐标
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            # 设置边界框颜色
            color = [int(c) for c in COLORS[classIDs[i]]]
            # 绘制边界框
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 3)
            # 计算中心点位置
            position = [x + w / 2, y + h / 2]
            positions.append(position)
            # 准备标签文本
            text = "{}".format(LABELS[classIDs[i]])
            # 绘制标签文本
            cv2.putText(image, text, (x, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            # 将10替换为T
            if LABELS[classIDs[i]] == '10':
                LABELS[classIDs[i]] = "T"

            # 保存检测结果
            class_list.append(LABELS[classIDs[i]])
            cen_list.append(position)
            c_list.append(position[0])
            pos_list.append([x, y, w, h])

    # 尝试对检测结果进行排序
    try:
        # 根据x坐标对检测结果进行排序
        _, class_list, pos_list = (list(t) for t in zip(*sorted(zip(c_list, class_list, pos_list), reverse=False)))
        return image, class_list, pos_list
    except:
        # 如果排序失败则返回None
        return image, None, None

