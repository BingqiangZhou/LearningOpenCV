'''
Author       : Bingqiang Zhou
Date         : 2021-02-17 16:33:11
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-17 16:55:56
Description  : OpenCV中图像二化自适应阈值算法
    OpenCV中的自适应阈值算法主要是基于均值实现，
    根据计算均值的方法不同分为盒子模糊均值与高斯模糊均值，
    然后使用原图减去均值图像，得到的差值图像进行自适应分割，
    相关的API如下：
        void cv::adaptiveThreshold(
        InputArray src,
        OutputArray dst,
        double maxValue,
        int adaptiveMethod,
        int thresholdType,
        int blockSize,
        double C
        )
    其中blockSize取值必须是奇数，C取值在10左右

    自适应方法类型：
    ADAPTIVE_THRESH_GAUSSIAN_C = 1
    ADAPTIVE_THRESH_MEAN_C = 0

    当阈值操作类型thresholdType为：THRESH_BINARY
    二值图像 = 原图 – 均值图像 > -C ? 255 : 0

    当阈值操作类型thresholdType为：THRESH_BINARY_INV
    二值图像 = 原图 – 均值图像 > -C ? 0 : 255
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/text1.png")
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

threshold, binary_THRESH_TRIANGLE = cv.threshold(gray, 0, 255, cv.THRESH_TRIANGLE)
print("THRESH_TRIANGLE threshold: ", threshold)

threshold, binary_THRESH_OTSU = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)
print("THRESH_OTSU threshold: ", threshold)


binary_ADAPTIVE_THRESH_GAUSSIAN_C = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)

binary_ADAPTIVE_THRESH_MEAN_C = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 25, 10)

# 可视化
rows = 2
cols = 3
images = [src, binary_THRESH_TRIANGLE, binary_THRESH_OTSU, binary_ADAPTIVE_THRESH_GAUSSIAN_C, binary_ADAPTIVE_THRESH_MEAN_C]
titles = ["original image", "THRESH_TRIANGLE", "THRESH_OTSU", "ADAPTIVE_THRESH_GAUSSIAN_C", "ADAPTIVE_THRESH_MEAN_C"]
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