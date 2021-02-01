'''
Author       : Bingqiang Zhou
Date         : 2021-02-02 04:53:10
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-02 05:04:05
Description  : 图像翻转(Image Flip)
    图像翻转的本质像素映射，OpenCV支持三种图像翻转方式
    - X轴翻转，flipcode = 0
    - Y轴翻转, flipcode = 1
    - XY轴翻转, flipcode = -1

    相关的API
    flip
    - src输入参数
    - dst 翻转后图像
    - flipcode
'''

import cv2 as cv
import numpy as np

# 读取图像
src = cv.imread("../data/images/cos.jpg")
cv.imshow("source image", src)

# 上下翻转 x flip
dst = cv.flip(src, 0)
cv.imshow("X flip", dst)

# 左右翻转 y flip
dst = cv.flip(src, 1)
cv.imshow("Y flip", dst)

## 上下左右同时翻转 x y flip
dst = cv.flip(src, -1)
cv.imshow("XY flip", dst)

## 自行实现 上下翻转
h, w, c = src.shape
temp = np.zeros_like(src)
for row in range(h):
    for col in range(w):
        temp[row, col] = src[h - row - 1, col]
        
cv.imshow("custom x flip", temp)

## 自行实现 水平翻转
h, w, c = src.shape
temp = np.zeros_like(src)
for row in range(h):
    for col in range(w):
        temp[row, col] = src[row, w - col - 1]

cv.imshow("custom Y flip", temp)


## 自行实现 上下左右同时翻转
h, w, c = src.shape
temp = np.zeros_like(src)
for row in range(h):
    for col in range(w):
        temp[row, col] = src[h - row - 1, w - col - 1]

cv.imshow("custom X Y flip", temp)

cv.waitKey(0)
cv.destroyAllWindows()
