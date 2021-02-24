'''
Author       : Bingqiang Zhou
Date         : 2021-02-24 21:40:14
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-24 22:31:46
Description  : 二值图像分析 – 提取最大轮廓与编码关键点
    提取星云的面积，做一些计算，其实在图像二值化的时候，我们需要考虑下面的因素，二值化方法选择：
        全局阈值二值化 threshold
        基于形态学梯度二值化 morphologyEx cv.MORPH_GRADIENT
        inRange二值化   inRange
        基于Canny边缘二值化 Canny
        自适应二值化 adaptiveThreshold
    我们在二值化方法选择上选择了全局阈值得到二值图像，然后进行轮廓分析，
    根据面积寻找最大轮廓，然后根据轮廓进行多边形逼近，获得轮廓关键点，
    最后可以绘制轮廓与关键点。
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

src = cv.imread("../data/images/cloud.jpg")

# 图像二值化
src = cv.GaussianBlur(src, (3, 3), 0)
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU) # 全局阈值二值化

# 闭操作，填充轮廓
kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
binary = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel)

# 轮廓提取
contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
areas = []
for c in range(len(contours)):
    area = cv.contourArea(contours[c])
    if area < 200: # 跳过过小的轮廓
        area = 0
    areas.append(area)
    # cv.rectangle(src, (x, y), (x+w, y+h), (0, 0, 255), 2)
    # cv.drawContours(src, contours, c, (0, 255, 0), 2)


max_indices = np.argmax(areas) # 获取最大的轮廓

# 提取星云区域
temp = src.copy()
h, w = temp.shape[:2]
for x in range(w):
    for y in range(h):
        in_contours = cv.pointPolygonTest(contours[max_indices], (x, y), False)
        temp[y, x] = src[y, x] if in_contours >= 0 else 0

# 画出轮廓以及关键点
cv.drawContours(src, contours, max_indices, (0, 255, 0), 2)
keypts = cv.approxPolyDP(contours[max_indices], 4, True)
for pt in keypts:
    cv.circle(src, tuple(pt[0, :]), 5, (0, 0, 255), -1)

# 可视化
rows = 1
cols = 3
images = [src, binary, temp]
titles = ["result", "binay", "cloud"]
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