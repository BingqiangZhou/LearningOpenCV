'''
Author       : Bingqiang Zhou
Date         : 2021-02-17 16:10:09
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-17 16:13:02
Description  : OpenCV中图像二值寻找算法 – OTSU
    图像二值化，除了我们上次分享的手动阈值设置与根据灰度图像均值的方法之外，
    还有几个根据图像直方图实现自动全局阈值寻找的方法，OpenCV中支持的有OTSU与Triangle两种直方图阈值寻找算法。
    其中OTSU的是通过计算类间最大方差来确定分割阈值的阈值选择算法，
    OTSU算法对直方图有两个峰，中间有明显波谷的直方图对应图像二值化效果比较好，
    而对于只有一个单峰的直方图对应的图像分割效果没有双峰的好。

    OpenCV中OTSU算法使用只需要在threshold函数的type类型声明THRESH_OTSU即可。
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/lena.jpg")
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

threshold, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)

# 可视化
rows = 1
cols = 2
images = [src, binary]
titles = ["original image", "THRESH_OTSU"]
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

