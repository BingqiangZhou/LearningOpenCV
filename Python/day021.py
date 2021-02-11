'''
Author       : Bingqiang Zhou
Date         : 2021-02-10 19:20:49
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-11 14:26:00
Description  : 图像卷积操作
    图像卷积可以看成是一个窗口区域在另外一个大的图像上移动，对每个窗口覆盖的区域都进行点乘得到的值作为中心像素点的输出值。
    窗口的移动是从左到右，从上到下。窗口可以理解成一个指定大小的二维矩阵，里面有预先指定的值。

    相关API
        dst	= cv.blur(src, ksize[, dst[, anchor[, borderType]]])
        卷积核所有值为1/(ksize.width*ksize.height)
        官方文档：https://docs.opencv.org/master/d4/d86/group__imgproc__filter.html#ga8c45db9afe636703801b0b2e440fce37
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def custom_3x3_blur(image):
    h, w, c = image.shape
    dst = np.copy(image)
    for row in range(1, h - 1):
        for col in range(1, w - 1):
            v1 = np.int32(image[row - 1, col - 1]) # v1-v9加到一起可能超过255，为了防止溢出，加大位宽
            v2 = np.int32(image[row - 1, col])
            v3 = np.int32(image[row - 1, col + 1])
            v4 = np.int32(image[row, col - 1])
            v5 = np.int32(image[row, col])
            v6 = np.int32(image[row, col + 1])
            v7 = np.int32(image[row + 1, col - 1])
            v8 = np.int32(image[row + 1, col])
            v9 = np.int32(image[row + 1, col + 1])
            
            for i in range(c):
                dst[row, col, i] = (v1[i] + v2[i] + v3[i] + v4[i] + v5[i] + v6[i] + v7[i] + v8[i] + v9[i]) // 9

    return dst

src = cv.imread("../data/images/lena.jpg")

dst_15x15 = cv.blur(src, (15, 15))

custom_dst = custom_3x3_blur(src)
dst_3x3 = cv.blur(src, (3, 3))

# 可视化
rows = 2
cols = 2

plt.subplot(rows, cols, 1)
plt.imshow(src[:, :, ::-1])

plt.subplot(rows, cols, 2)
plt.imshow(dst_15x15[:, :, ::-1])

plt.subplot(rows, cols, 3)
plt.imshow(dst_3x3[:, :, ::-1])

plt.subplot(rows, cols, 4)
plt.imshow(custom_dst[:, :, ::-1])

plt.show()
