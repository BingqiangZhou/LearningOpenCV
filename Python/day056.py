'''
Author       : Bingqiang Zhou
Date         : 2021-02-23 00:17:43
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-23 00:49:37
Description  : 二值图像分析 – 直线拟合与极值点寻找
    对轮廓进行分析，除了可以对轮廓进行椭圆或者圆的拟合之外，还可以对轮廓点集进行直线拟合，
    直线拟合的算法有很多，最常见的就是最小二乘法，对于多约束线性方程，
    最小二乘可以找好直线方程的两个参数、实现直线拟合，OpenCV中直线拟合正是基于最小二乘法实现的。
    OpenCV实现直线拟合的API如下：
        void cv::fitLine(
            InputArray points,
            OutputArray line,
            int distType,
            double param,
            double reps,
            double aeps 
        )
    points表示待拟合的输入点集合
    line在二维拟合时候输出的是vec4f类型的数据，在三维拟合的时候输出是vec6f的vector
    distType表示在拟合时候使用距离计算公式是哪一种，OpenCV支持如下六种方式：
        DIST_L1 = 1
        DIST_L2 = 2
        DIST_L12 = 4
        DIST_FAIR = 5
        DIST_WELSCH = 6
        DIST_HUBER = 7
    param对模型拟合距离计算公式需要参数C，5~7 distType需要参数C
    reps与aeps是指对拟合结果的精度要求
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

src = cv.imread("../data/images/twolines.png")

t = 80
binary = cv.Canny(src, t, t*2) # 边缘检测
# gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
# thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)
k = np.ones((3, 3), dtype=np.uint8)
# 膨胀，最大值滤波，卷积核与图像做卷积，即计算卷积核覆盖的区域的像素点的最大值，并把这个最大值赋值给参考点指定的像素
binary = cv.morphologyEx(binary, cv.MORPH_DILATE, k) 

# 发现轮廓
contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
for c in range(len(contours)):
    
    # 跳过外接矩阵最大长宽不超过50的轮廓
    x, y, w, h = cv.boundingRect(contours[c])
    m = max(w, h)
    if m < 50:
        continue

    line = cv.fitLine(contours[c], cv.DIST_L1, 0, 0.01, 0.01)
    dx, dy, x0, y0 = line # dx、dy分别为x轴、y轴的变化率，x0与y0为直线上的一个点
    k = dy / dx # 斜率
    b = y0 - k * x0 # 截距
    print(f"line {c}", k, b, x0, y0)

    # 寻找极值点
    minx = np.min(contours[c][:, 0, 0])
    maxx = np.max(contours[c][:, 0, 0])
    # miny = np.min(contours[c][:, 0, 1])
    # maxy = np.max(contours[c][:, 0, 1])

    # 通过minx、maxx计算得到miny、maxy，也可以通过miny、maxy来计算minx、max
    miny = k * minx + b
    maxy = k * maxx + b
    # print(minx, miny, maxx, maxy)
    
    # 画出拟合的直线
    cv.line(src, (minx, miny), (maxx, maxy), (0, 0, 255), 2)

# 可视化 
rows = 1
cols = 2
images = [binary, src]
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
