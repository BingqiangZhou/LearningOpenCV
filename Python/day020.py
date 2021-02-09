'''
Author       : Bingqiang Zhou
Date         : 2021-02-09 19:10:53
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-10 01:43:44
Description  : 图像直方图反向投影
    文字解释：图像直方图反向投影是通过构建指定模板图像的二维直方图空间与目标的二维直方图空间，
    进行直方图数据归一化之后，进行比率操作，对所有得到非零数值，
    生成查找表对原图像进行像素映射之后，再进行图像模糊输出的结果。

    通俗来说就是
    给一个模版图像和一个目标图像，在目标图像中找模版图像的响应位置，再通过查找表映射输出一个表示响应值大小的图像
    最后适用卷积模糊降低反向投影之后图像结果的噪声

    直方图反向投影流程：
    - 计算直方图
    - 归一化输出
    - 计算比率R
    - LUT查找表
    - 卷积模糊

    相关API
    - calcBackProject(images, channels, hist, ranges, scale[, dst])
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

sample = cv.imread("../data/images/sample.png")
target = cv.imread("../data/images/target.png")

# 转到HSV空间
roi_hsv = cv.cvtColor(sample, cv.COLOR_BGR2HSV)
target_hsv = cv.cvtColor(target, cv.COLOR_BGR2HSV)

# 计算直方图
roi_hist = cv.calcHist([roi_hsv], [0, 1], None, [32, 32], [0, 180, 0, 256])

# normlize到[0, 255]
cv.normalize(roi_hist, roi_hist, 0, 255, norm_type=cv.NORM_MINMAX)

# 图像直方图反向投影
dst = cv.calcBackProject([target_hsv], [0, 1], roi_hist, [0, 180, 0, 256], 1)

# 可视化
rows = 2
cols = 2
plt.subplot(rows, cols, 1)
plt.imshow(sample[:, :, ::-1])  # bgr to rgb

plt.subplot(rows, cols, 2)
plt.imshow(target[:, :, ::-1])

plt.subplot(rows, cols, 3)
plt.imshow(roi_hist)            # 2d hist

plt.subplot(rows, cols, 4)
plt.imshow(dst)

plt.show()