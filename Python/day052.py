'''
Author       : Bingqiang Zhou
Date         : 2021-02-22 15:43:19
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-22 16:22:20
Description  : 二值图像分析 – 使用几何矩计算轮廓中心与横纵比过滤
    对图像二值图像的每个轮廓，可以计算轮廓几何矩，
    根据几何矩可以计算图像的中心位置，估计得到中心位置可以计算中心矩、然后再根据中心矩可以计算胡矩。
    OpenCV中可以通过如下的API一次计算出上述三种矩，API如下：
    Moments cv::moments(
        InputArray 	array,
        bool binaryImage = false
    )
    array是输入的图像轮廓点集合
    输出的图像几何矩。
    如何计算中心位置等，参考文档中细节描述部分：https://docs.opencv.org/4.5.1/d8/d23/classcv_1_1Moments.html
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

    mm = cv.moments(contours[c])
    m00 = mm["m00"]
    m10 = mm["m10"]
    m01 = mm["m01"]
    cx = int(m10 /m00)
    cy = int(m01 /m00)
    print("moments: ",cx, cy) # 注意: 轮廓的中心与外接矩阵的中心坐标不一定一致

    rect = cv.minAreaRect(contours[c]) # 获取轮廓最小外接矩形
    cx, cy = rect[0] # 获取外接矩形中心坐标
    print("rect: ", cx, cy)
    w, h = rect[1] # 获取高宽
    ratio = min(h, w) / max(h, w) # 高宽比
    box = cv.boxPoints(rect) # 通过矩形的左上角和高宽获得矩形的四个点的坐标
    box = np.int0(box) # int0是intp的别名（alias），根据32位、64位机器对应int32、int64
    if ratio > 0.9: #高宽比大于0.9
        color = (0, 0, 255)
    elif ratio < 0.5:
        color = (0, 255, 0)
    else:
        color = (255, 0, 0)
    cv.drawContours(src, [box], 0, color, 2, cv.LINE_8) # 绘制矩形框
    cv.circle(src, (int(cx), int(cy)), 5, color, cv.FILLED) # 绘制中心点

# 可视化 
rows = 1
cols = 2
images = [binary, src]
titles = ["binary image", "image"]
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

