'''
Author       : Bingqiang Zhou
Date         : 2021-02-22 14:05:28
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-22 15:11:29
Description  : 二值图像分析 – 矩形面积与弧长
    对图像二值图像的每个轮廓，我们可以计算轮廓的弧长与面积，
    根据轮廓的面积与弧长可以实现对不同大小对象的过滤，寻找到我们感兴趣的roi区域，这个也是图像二值分析的任务之一。
    OpenCV对轮廓点集计算面积的API函数如下
        double cv::contourArea(
        InputArray 	contour,
        bool oriented = false
        )
    计算轮廓的面积，其原理是基于格林公式。
    参数contour表示输入的轮廓点集
    参数oriented默认是false返回的面积是正数，如果方向参数为true表示会根据是顺时针或者逆时针方向返回正值或者负值面积。

        double cv::arcLength(
        InputArray curve,
        bool closed 
        )
    计算轮廓曲线的弧长。
    参数curve表示输入的轮廓点集
    参数closed默认表示是否闭合区域
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

src = cv.imread("../data/images/zhifang_ball.png")

t = 80
binary = cv.Canny(src, t, t*2) # 边缘检测
k = np.ones((3, 3), dtype=np.uint8)
# 膨胀，最大值滤波，卷积核与图像做卷积，即计算卷积核覆盖的区域的像素点的最大值，并把这个最大值赋值给参考点指定的像素
binary = cv.morphologyEx(binary, cv.MORPH_DILATE, k)

temp1 = src.copy()
temp2 = src.copy()
# 发现轮廓
contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# print(hierarchy, hierarchy.shape)
for c in range(len(contours)):
    # 绘制轮廓，每次画轮廓中的第c个
    cv.drawContours(src, contours, c, (0, 0, 255), 2, cv.LINE_8)
    # cv.drawContours(src, contours, c, (0, 0, 255), cv.FILLED, cv.LINE_8)
    
    # 跳过绘制子层结构
    if hierarchy[0][c][3] != -1:
        continue
    area = cv.contourArea(contours[c]) # 计算轮廓区域面积
    arc = cv.arcLength(contours[c], True) # 计算轮廓弧长
    # 跳过绘制面积小于100、或者弧长小于100的轮廓
    if area < 100 or arc < 100:
        continue
    cv.drawContours(temp1, contours, c, (0, 0, 255), 2, cv.LINE_8)
    rect = cv.minAreaRect(contours[c]) # 获取轮廓最小外接矩形
    cx, cy = rect[0] # 获取中心坐标
    box = cv.boxPoints(rect) # 通过矩形的左上角和高宽获得矩形的四个点的坐标
    box = np.int0(box) # int0是intp的别名（alias），根据32位、64位机器对应int32、int64
    cv.drawContours(temp2, [box], 0, (0, 0, 255), 2, cv.LINE_8) # 绘制矩形框
    cv.circle(temp2, (int(cx), int(cy)), 5, (0, 0, 255), cv.FILLED) # 绘制中心点


# 可视化 
rows = 2
cols = 2
images = [binary, src, temp1, temp2]
titles = ["binary image", "all", "part", "part rect"]
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
