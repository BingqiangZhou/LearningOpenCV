'''
Author       : Bingqiang Zhou
Date         : 2021-02-23 11:27:54
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-23 11:39:13
Description  : 二值图像分析 – 霍夫直线检测二
    OpenCV中还有另外一个霍夫直线检测的API，该API更为常用，它会直接返回直线的空间坐标点，
    比返回霍夫空间参数更加的直观，容易理解，而且还可以声明线段长度、间隔等参数，非常有用。
    该参数详解如下：
        void cv::HoughLinesP(
            InputArray image,
            OutputArray lines,
            double rho,
            double theta,
            int threshold,
            double 	minLineLength = 0,
            double 	maxLineGap = 0 
        )
    Image输入二值图像
    Lines 返回的直线两个点
    Rho 极坐标r得步长
    Theta角度步长
    Threshold累加器阈值
    minLineLength最小线段长度
    maxLineGap线段间隔
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# src = cv.imread("../data/images/sudoku.png")
src = cv.imread("../data/images/morph01.png")

t = 80
binary = cv.Canny(src, t, t*2) # 边缘检测

lines = cv.HoughLinesP(binary, 1, np.pi / 180.0, 50, minLineLength=50, maxLineGap=10)

result = np.zeros_like(src)
for i in range(len(lines)):
    pt1 = (lines[i][0][0], lines[i][0][1])
    pt2 = (lines[i][0][2], lines[i][0][3])
    cv.line(result, pt1, pt2, (0, 0, 255), 2)

# 可视化 
rows = 1
cols = 3
images = [src, binary, result]
titles = ["original image", "binary image"]
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
