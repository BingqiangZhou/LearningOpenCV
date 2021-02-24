'''
Author       : Bingqiang Zhou
Date         : 2021-02-24 19:39:00
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-24 21:34:32
Description  : 二值图像分析案例 – 缺陷检测二
    对于得到的刀片外接矩形，首先需要通过排序，确定他们的编号，
    然后根据模板进行相减得到与模板不同的区域，对这些区域进行形态学操作，
    去掉边缘细微差异，最终就得到了可以检出的缺陷或者划痕刀片。
'''

import cv2 as cv
import numpy as np
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
boxes = []
for c in range(len(contours)):
    x, y, w, h = cv.boundingRect(contours[c])
    area = cv.contourArea(contours[c])
    if area < 150: # 去掉过小的轮廓
        continue
    if h > (height // 2): # 去掉外层大框框
        continue
    cv.rectangle(src, (x, y), (x+w, y+h), (0, 0, 255), 2)
    cv.drawContours(src, contours, c, (0, 255, 0), 2)
    boxes.append([x, y, w, h])

# 将刀片边框信息按上到下排序
boxes = np.array(boxes)
indices = np.argsort(boxes[:, 1])[::-1] # 按y从大到小排列
boxes = boxes[indices]
# print(rects)

# 将第index个作为好的模版用于对比
index = 2
roi_x, roi_y, roi_w, roi_h = boxes[index]
template_roi = binary[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

# 缺陷检测
for x, y, w, h in boxes:
    detect_roi = binary[y:y+h, x:x+w]
    detect_roi = cv.resize(detect_roi, (roi_w, roi_h))
    mask = cv.subtract(template_roi, detect_roi) # 模版与检测区域相减，得到差距
    
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel) # 开操作，去掉过小的（区域）差别
    thresh, mask = cv.threshold(mask, 0, 255, cv.THRESH_OTSU) # 二值化
    if np.all(mask == 0): # 检测为好的刀片
        cv.putText(src, "good", (x, y), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    else:
        cv.putText(src, "bad", (x, y), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

# 可视化
rows = 1
cols = 3
images = [src, binary, template_roi]
titles = ["result", "binary", "roi"]
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
