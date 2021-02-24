'''
Author       : Bingqiang Zhou
Date         : 2021-02-24 19:36:28
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-24 22:30:35
Description  : 二值图像分析案例 – 缺陷检测一
    二值图像分析的案例，通过这些案例知识把前面所学的知识点串联起来使用，实现有一定工业实用价值的代码。
    缺陷检测一，分为两个部分，一个部分是提取指定的轮廓，第二个部分通过对比实现划痕检测与缺角检测。
    本次分享主要搞定第一部分，学会观察图像与提取图像ROI对象轮廓外接矩形与轮廓。
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/ce01.jpg")

# 图像二值化
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY_INV)

# 开操作去掉小块干扰
kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3), (-1, -1)) 
binary = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)

# 轮廓提取
contours, hierarchy = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
height, width = src.shape[:2]
for c in range(len(contours)):
    x, y, w, h = cv.boundingRect(contours[c])
    area = cv.contourArea(contours[c])
    if area < 150: # 去掉过小的轮廓
        continue
    if h > (height // 2): # 去掉外层大框框
        continue
    cv.rectangle(src, (x, y), (x+w, y+h), (0, 0, 255), 2)
    cv.drawContours(src, contours, c, (0, 255, 0), 2)

# 可视化
rows = 1
cols = 2
images = [src, binary]
titles = ["result", "binay"]
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

