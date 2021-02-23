'''
Author       : Bingqiang Zhou
Date         : 2021-02-23 22:42:44
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-23 23:20:29
Description  : 形态学应用 – 使用基本梯度实现轮廓分析
    基于形态学梯度实现图像二值化，进行文本结构分析是OCR识别中常用的处理手段之一，
    这种好处比简单的二值化对图像有更好的分割效果，主要步骤如下：
        1.	图像形态学梯度
        2.	灰度
        3.	全局阈值二值化
        4.	轮廓分析
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/kd.jpeg")

# 1.图像形态学梯度（获取到轮廓）
kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
gradient = cv.morphologyEx(src, cv.MORPH_GRADIENT, kernel)

# 2.灰度
gray = cv.cvtColor(gradient, cv.COLOR_BGR2GRAY)

# 3.全局阈值二值化
thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)

# 4.轮廓分析
kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 10))
binary = cv.morphologyEx(binary, cv.MORPH_DILATE, kernel)
contours, hierarcy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
for c in range(len(contours)):
    x, y, w, h = cv.boundingRect(contours[c])
    area = cv.contourArea(contours[c])
    if area < 200:
        continue
    if h > (3*w) or h < 20:
        continue
    cv.rectangle(src, (x, y), (x+w, y+h), (0, 0, 255), 2)

# 可视化
rows = 2
cols = 2
images = [src, gradient, gray, binary]
titles = ["original image", "MORPH_GRADIENT", "gray", "binary"]
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
