'''
Author       : Bingqiang Zhou
Date         : 2021-02-24 22:33:52
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-24 22:58:58
Description  : 图像去水印/修复
    在OpenCV中有时候我们需要一个批量的去水印的方法，这个在很多时候需要用到，对得到图像进行批量的去水印，
    其本质上是一种图像修复，OpenCV也提供一个图像修复的API，可以部分解决这里问题，
        void cv::inpaint(
        InputArray  src,
        InputArray  ipaintMask,
        OutputArray  dst
        double  npaintRadius,
        int  fags 
        )
    基于Navier-Stokes的修复方法
    基于图像梯度的快速匹配方法又称(Telea法)
'''

import cv2 as cv
import matplotlib.pyplot as plt

# src = cv.imread("../data/images/master2.jpg")
src = cv.imread("../data/images/wm.jpg")

# 获取需要去掉区域(水印)
hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv, (100, 43, 46), (124, 255, 255))

kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
mask = cv.morphologyEx(mask, cv.MORPH_DILATE, kernel) # 膨胀

# 图像修复
result = cv.inpaint(src, mask, 3, cv.INPAINT_TELEA)
result_ns = cv.inpaint(src, mask, 3, cv.INPAINT_NS)

# 可视化
rows = 2
cols = 2
images = [src, mask, result, result_ns]
titles = ["original image", "mask", "INPAINT_TELEA", "INPAINT_NS"]
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