'''
Author       : Bingqiang Zhou
Date         : 2021-02-23 00:51:31
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-23 01:26:00
Description  : 二值图像分析 – 点多边形测试
    对于轮廓图像，有时候还需要判断一个点是在轮廓内部还是外部，OpenCV中实现这个功能的API叫做点多边形测试，
    它可以准确的得到一个点距离多边形的距离，如果点是轮廓点或者属于轮廓多边形上的点，距离是零，
    如果是多边形内部的点是是正数，如果是负数返回表示点是外部。表示如下：
        double cv::pointPolygonTest(
            InputArray contour,
            Point2f pt,
            bool measureDist 
        )
    Contour轮廓所有点的集合
    Pt 图像中的任意一点
    MeasureDist
        如果是True，则返回每个点到最近轮廓的距离（distance between the point and the nearest contour edge），
        如果是False则返回+1，0，-1三个值，其中+1表示点在轮廓内部，0表示点在轮廓上，-1表示点在轮廓外
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

src = cv.imread("../data/images/mask.png")

t = 80
binary = cv.Canny(src, t, t*2) # 边缘检测
# gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
# thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)
k = np.ones((3, 3), dtype=np.uint8)
# 膨胀，最大值滤波，卷积核与图像做卷积，即计算卷积核覆盖的区域的像素点的最大值，并把这个最大值赋值给参考点指定的像素
binary = cv.morphologyEx(binary, cv.MORPH_DILATE, k) 

# 发现轮廓
contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

result = np.zeros_like(src, dtype=np.float32) # 注意数据类型
h, w = result.shape[:2]
for row in range(h):
    for col in range(w):
        dist = cv.pointPolygonTest(contours[0], (col, row), True)
        if dist > 0: # 在多边形内
            result[row, col] = (255-dist, 0, 0)
        elif dist < 0: # 在多边形外
            result[row, col] = (0, 0, 255-dist)
        else: # dist == 0，在多边形边缘上
            result[row, col] = (0, 255, 0)

result = cv.convertScaleAbs(result)

# 可视化 
rows = 1
cols = 2
images = [binary, result]
titles = ["binary image"]
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

