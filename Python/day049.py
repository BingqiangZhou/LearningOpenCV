'''
Author       : Bingqiang Zhou
Date         : 2021-02-22 12:56:31
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-22 14:15:12
Description  : 二值图像分析 – 轮廓外接矩形
    对图像二值图像的每个轮廓，OpenCV都提供了API可以求取轮廓的外接矩形，
    其中求取轮廓外接矩形有两种方式，一种是可以基于像素的最大外接轮廓矩形，API解释如下：
        Rect cv::boundingRect(
        InputArray points
        )

    输入参数points可以一系列点的集合，对轮廓来说就是该轮廓的点集
    返回结果是一个矩形，x, y, w, h

    最小的外接轮廓矩形
        RotatedRect cv::minAreaRect(
        InputArray points
        )

    输入参数points可以一系列点的集合，对轮廓来说就是该轮廓的点集
    返回结果是一个旋转矩形，包含下面的信息：
    -	矩形中心位置
    -	矩形的宽高
    -	旋转角度
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

src = cv.imread("../data/images/stuff.jpg")

t = 80
binary = cv.Canny(src, t, t*2) # 边缘检测
k = np.ones((3, 3), dtype=np.uint8)
# 膨胀，最大值滤波，卷积核与图像做卷积，即计算卷积核覆盖的区域的像素点的最大值，并把这个最大值赋值给参考点指定的像素
binary = cv.morphologyEx(binary, cv.MORPH_DILATE, k) 

# 发现轮廓
contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# print(hierarchy, hierarchy.shape)
# print(len(contours))
temp = src.copy()
for c in range(len(contours)):

    x, y, w, h = cv.boundingRect(contours[c]) # 最大外接轮廓矩形
    cv.rectangle(src, (x, y), (x+w, y+h), (0, 0, 255), 2, cv.LINE_8) # 绘制矩形框

    rect = cv.minAreaRect(contours[c]) # 获取轮廓最小外接矩形
    cx, cy = rect[0] # 获取中心坐标
    box = cv.boxPoints(rect) # 通过矩形的左上角和高宽获得矩形的四个点的坐标
    box = np.int0(box) # int0是intp的别名（alias），根据32位、64位机器对应int32、int64
    cv.drawContours(temp, [box], 0, (0, 0, 255), 2, cv.LINE_8) # 绘制矩形框
    cv.circle(temp, (int(cx), int(cy)), 5, (0, 0, 255), cv.FILLED) # 绘制中心点

# 可视化 
rows = 1
cols = 3
images = [binary, src, temp]
titles = ["binary image", "boundingRect", "minAreaRect"]
plt.figure(figsize=(cols * 4, rows * 3)) # Width, height in inches.
for index, image in enumerate(images):
    plt.subplot(rows, cols, index + 1)
    if index >= len(titles):
        plt.title("image")
    else:
        plt.title(titles[index])
    plt.axis("off")
    if image.ndim > 2:
        plt.imshow(image[:, :, ::-1])
    else:
        plt.imshow(image, cmap="gray")
plt.show()

