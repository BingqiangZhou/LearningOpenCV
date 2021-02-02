'''
Author       : Bingqiang Zhou
Date         : 2021-02-02 22:01:49
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-03 00:20:26
Description  : 几何形状绘制
    绘制几何形状
        - 绘制直线
        - 绘制圆
        - 绘制矩形
        - 绘制椭圆
    填充几何形状
        OpenCV没有专门的填充方法，只是把绘制几何形状时候的线宽 - thickness参数值设置为负数即表示填充该几何形状或者使用参数CV_FILLED
        线的类型有3种：LINE_4（四邻域）、LINE_8（8邻域）、LINE_AA （抗锯齿，antialiased）
    随机数方法：
        RNG 表示OpenCV C++版本中的随机数对象，rng.uniform(a, b)生成[a, b)之间的随机数，包含a，但是不包含b。
        np.random.rand() 表示numpy中随机数生成，生成浮点数0～1的随机数, 包含0，不包含1。
'''

import cv2 as cv
import numpy as np
from random import randint, random

canvas = np.zeros((512, 512, 3))

# 画线 (图像对象，起始点，结束点，bgr颜色，线宽，线的类型，点坐标中的二进制右移位数)
# thickness参数值设置为负数即表示填充该几何形状或者使用参数CV_FILLED
# 线的类型有3种：LINE_4（四邻域）、LINE_8（8邻域）、LINE_AA （抗锯齿，antialiased）
# shift是将坐标值二进制右移的位数, v/(2**shift)
cv.line(canvas, (0, 0), (512, 512), (0, 0, 255), thickness=10, lineType=cv.LINE_4, shift=0)

# 画矩形 参数与画线一致 (图像对象，起始点，结束点，bgr颜色，线宽，线的类型，点坐标中的二进制右移位数)，起始坐标（8， 8）结束坐标（256， 256）
cv.rectangle(canvas, (2**5, 2**5), (2**10, 2**10), (0, 255, 0), thickness=3, lineType=cv.LINE_8, shift=2)

# 画圆 (图像对象，圆心，半径，bgr颜色，线宽，线的类型，点坐标中的二进制右移位数)
cv.circle(canvas, (256, 256), 200, (255, 0, 0), thickness=5, lineType=cv.LINE_8, shift=0)

# 画椭圆 (图像对象，圆心，水平轴与竖直轴长度，画多少度，开始画的角度，结束的角度，bgr颜色，线宽，线的类型，点坐标中的二进制右移位数)
cv.ellipse(canvas, (256, 256), axes=(150, 200), angle=360, startAngle=0, endAngle=360, \
    color=(255, 255, 0), thickness=-1, lineType=cv.LINE_AA, shift=0)
cv.ellipse(canvas, (256, 256), axes=(200, 150), angle=360, startAngle=0, endAngle=360, \
    color=(255, 255, 0), thickness=cv.FILLED, lineType=cv.LINE_AA, shift=0)

cv.imshow("canvas", canvas)

# 重置画布（将图像三个通道都置为0）
canvas[:, :, :] = 0

# 随机画线(画矩形)的位置、颜色

h, w = canvas.shape[:2]
for i in range(int(1e3)):
    # canvas[:, :, :] = 0

    # 随机起始坐标、结束坐标
    # x1 = np.random.rand() * w
    # y1 = np.random.rand() * h
    # x2 = np.random.rand() * w
    # y2 = np.random.rand() * h

    # 用python自带random库代替np.random
    x1 = random() * w
    y1 = random() * h
    x2 = random() * w
    y2 = random() * h

    # 随机颜色值
    # b = np.random.randint(0, 256)
    # g = np.random.randint(0, 256)
    # r = np.random.randint(0, 256)

    # 用python自带random库代替np.random
    b = randint(0, 256)
    g = randint(0, 256)
    r = randint(0, 256)

    cv.line(canvas, (int(x1), int(y1)), (int(x2), int(y2)), (b, g, r), thickness=1, lineType=cv.LINE_8, shift=0)
    # cv.rectangle(canvas, (int(x1), int(y1)), (int(x2), int(y2)), (b, g, r), thickness=1, lineType=cv.LINE_8, shift=0)

    cv.imshow("random draw", canvas)

    c = cv.waitKey(10)
    if c == 27: # ESC
        break
    
cv.waitKey(0)
cv.destroyAllWindows()
