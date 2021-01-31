'''
Author       : Bingqiang Zhou
Date         : 2021-01-31 23:51:35
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-01 00:29:40
Description  : 图像通道分离与合并
    通道分离 - split
    通道合并 - merge
    混合通道 - mixChannels 将输入数组的指定通道复制到输出数组的指定通道
'''

import cv2 as cv
import numpy as np

src = cv.imread("../data/images/cos.jpg")
cv.imshow("source image", src)

## 通道分离
b, g, r = cv.split(src)
cv.imshow("blue", b)
cv.imshow("green", g)
cv.imshow("red", r)

## 通道合并，将一个通道所有值设置为0再合并
for i in range(3):
    bgr = cv.split(src)
    bgr[i][:, :] = 0 # 将第i个通道设置为0
    dst = cv.merge(bgr)
    cv.imshow("merge channel without {}".format(i), dst)

## mixChannels 将输入数组的指定通道复制到输出数组的指定通道

# 需要初始化输出矩阵的大小
dst = np.zeros_like(src)
# 两个两个一组，0，1；1，2；2，0，src的第一个通道放到dst第二个换，src的第二个通道与放到dst第三个，src的第三个通道与放到dst第一个通道
from_to = [0, 1, 1, 2, 2, 0]
# 加上[]，将src和dst变成列表，否则结果不正常，参考：https://stackoverflow.com/questions/42329901/opencv-python-cv2-mixchannels
cv.mixChannels([src], [dst], from_to) 
cv.imshow("mixChannels", dst)

cv.waitKey(0)
cv.destroyAllWindows()
