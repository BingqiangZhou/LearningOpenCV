'''
Author       : Bingqiang Zhou
Date         : 2021-02-14 12:45:50
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-14 13:05:48
Description  : 边缘保留滤波算法 – 均值迁移模糊(mean-shift blur)
    均值迁移模糊是图像边缘保留滤波算法中一种，经常用来在对图像进行分水岭分割之前去噪声，可以大幅度提升分水岭分割的效果。
    均值迁移模糊的主要思想如下：
        在图像进行开窗的时候同时，考虑像素值空间范围分布，只有符合分布的像素点才参与计算，计算得到像素均值与空间位置均值，
        使用新的均值位置作为窗口中心位置继续基于给定像素值空间分布计算均值与均值位置，
        如此不断迁移中心位置直到不再变化位置（dx=dy=0），但是在实际情况中我们会人为设置一个停止条件比如迁移几次，
        这样就可以把最后的RGB均值赋值给中心位置。

    OpenCV中均值迁移滤波的API函数：
        dst=cv.pyrMeanShiftFiltering(	src, sp, sr[, dst[, maxLevel[, termcrit]]])
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/example.png")

dst1 = cv.pyrMeanShiftFiltering(src, 15, 30)

# 可视化
rows = 1
cols = 2
images = [src, dst1]
titles = ["original image", "pyrMeanShiftFiltering"]
for index, image in enumerate(images):
    plt.subplot(rows, cols, index + 1)
    if index >= len(titles):
        plt.title("image")
    else:
        plt.title(titles[index])
    plt.axis("off")
    plt.imshow(image[:, :, ::-1])
plt.show()