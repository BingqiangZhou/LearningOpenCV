'''
Author       : Bingqiang Zhou
Date         : 2021-02-17 14:33:13
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-17 14:54:02
Description  : 二值图像介绍
    二值图像就是只有黑白两种颜色表示的图像，其中0 – 表示黑色， 1 – 表示白色(255) 。
    二值图像处理与分析在机器视觉与机器人视觉中非常重要，涉及到非常多的图像处理相关的知识，
    常见的二值图像分析包括轮廓分析、对象测量、轮廓匹配与识别、形态学处理与分割、各种形状检测与拟合、投影与逻辑操作、轮廓特征提取与编码等。
    此外图像二值化的方法也有很多，OpenCV主要是支持几种经典的二值化算法。
    从编程与代码角度，OpenCV中二值图像单通道的、字节类型的Mat对象、
    对于任意的输入图像首先需要把图像转换为灰度、然后通过二值化方法转换为二值图像。
    本质上，从灰度到二值图像，是对数据的二分类分割，所以很多数据处理的方法都可以使用，
    但是图像是特殊类型的数据，它有很多限制条件，决定了只有一些合适的方法才会取得比较好的效果。
    这些算法的最主要的一个任务就是寻找合理的分割阈值T、对于给定任意一个像素点灰度值
    P(x, y) > T ? 255 :  0
    多数人接触二值图像都是从下面的这个程序实现二值分割的，就是使用T=127作为阈值，对灰度图像进行二值分割。
'''

import cv2 as cv
import numpy as np

src = cv.imread("../data/images/lena.jpg")
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

# 设置阈值
t = 127
# t = cv.mean(gray)[0] # 将均值作为阈值

# 二值分割
# h, w = gray.shape
# binary = np.zeros((h, w), dtype=np.uint8)
# for row in range(h):
#     for col in range(w):
#         v = gray[row, col]
#         if v > t:
#             binary[row, col] = 255
#         else:
#             binary[row, col] = 0

binary = np.zeros_like(gray, dtype=np.uint8)
binary[gray > t] = 255 # 等价于上述31～39行代码


# 可视化
images = [src, binary]
titles = ["original image", "binary"]
for index, image in enumerate(images):
    cv.imshow(titles[index], image)
    
cv.waitKey(0)
