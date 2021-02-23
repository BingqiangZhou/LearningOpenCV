'''
Author       : Bingqiang Zhou
Date         : 2021-02-23 10:33:59
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-23 11:27:30
Description  : 二值图像分析 – 霍夫直线检测
    图像霍夫变换是一种特别有用的图像变换，通过把图像的坐标从2D平面坐标系变换到极坐标空间，
    可以发现原来在平面坐标难以提取的几何特征信息（如：直线、圆等），
    图像的直线与圆检测就是典型的利用霍夫空间特性实现二值图像几何分析的例子。
    假设有如下的直线参数方程：
        r = x*cos(theta) + y * sin(theta)
    其中角度theta指r与X轴之间的夹角，r为到直线几何垂直距离。

    OpenCV关于霍夫直线检测有两个API，第一个函数，它是提取到直线在霍夫空间得几何特征，然后输出直线得两个极坐标参数。
    根据这两个参数我们可以组合得到空间坐标直线。该API如下：
        void cv::HoughLines(
            InputArray  image,
            OutputArray lines,
            double rho,
            double theta,
            int threshold,
            double srn = 0,
            double stn = 0,
            double min_theta = 0,
            double max_theta = CV_PI
        )
        Image 输入图像
        Lines 输出直线
        Rho 极坐标r得步长
        Theta角度步长
        Threshold累加器阈值
        Srn、stn多尺度霍夫变换时候需要得参数，经典霍夫变换不需要
        min_theta 最小角度
        max_theta最大角度
    
    参考链接：
        霍夫变换直线检测（Line Detection）原理及示例 - https://blog.csdn.net/leonardohaig/article/details/87907462
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

src = cv.imread("../data/images/sudoku.png")

t = 80
binary = cv.Canny(src, t, t*2) # 边缘检测

lines = cv.HoughLines(binary, 1, np.pi / 180.0, 150)

result = src.copy()
for i in range(len(lines)):
    rho = lines[i][0][0]
    theta = lines[i][0][1]
    a = np.cos(theta) 
    b = np.sin(theta) 
    x0 = rho * a   
    y0 = rho * b
    scale = 1000 # 从（x0，y0）延长，得到两个点
    pt1 = (int(x0 - scale * (b)), int(y0 + scale * (a)))
    pt2 = (int(x0 + scale * (b)), int(y0 - scale * (a)))
    cv.line(result, tuple(pt1), tuple(pt2), (0, 0, 255), 2)

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
