'''
Author       : Bingqiang Zhou
Date         : 2021-02-17 16:23:40
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-17 16:24:58
Description  : OpenCV中图像二值寻找算法 – TRIANGLE
    图像二值化，除了我们上次分享的手动阈值设置与根据灰度图像均值的方法之外，
    还有几个根据图像直方图实现自动全局阈值寻找的方法，OpenCV中支持的有OTSU与Triangle两种直方图阈值寻找算法。
    上次分享提到OTSU基于类内最小方差实现阈值寻找, 它对有两个波峰之间有一个波谷的直方图特别好,
    但是有时候图像的直方图只有一个波峰,这个时候使用TRIANGLE方法寻找阈值是比较好的一个选择。

    OpenCV中TRIANGLE算法使用只需要在threshold函数的type类型声明THRESH_TRIANGLE即可。
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/lena.jpg")
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

threshold, binary = cv.threshold(gray, 0, 255, cv.THRESH_TRIANGLE)
print("threshold: ", threshold)

# 可视化
rows = 1
cols = 2
images = [src, binary]
titles = ["original image", "THRESH_TRIANGLE"]
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

