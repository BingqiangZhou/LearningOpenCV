'''
Author       : Bingqiang Zhou
Date         : 2021-02-14 14:39:09
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-14 15:50:55
Description  : 快速的图像边缘滤波算法
    高斯双边模糊与mean shift均值模糊两种边缘保留滤波算法，都因为计算量比较大，无法实时实现图像边缘保留滤波，限制了它们的使用场景，
    OpenCV中还实现了一种快速的边缘保留滤波算法。高斯双边与mean shift均值在计算时候使用五维向量是其计算量大速度慢的根本原因，
    该算法通过等价变换到低纬维度空间，实现了数据降维与快速计算。

    OpenCV API函数为：
    
    dst	= cv.edgePreservingFilter(	src[, dst[, flags[, sigma_s[, sigma_r]]]])

    其中sigma_s的取值范围为0～200， sigma_r的取值范围为0～1
    当sigma_s取值不变时候，sigma_r越大图像滤波效果越明显
    当sigma_r取值不变时候，窗口sigma_s越大图像模糊效果越明显
    当sgma_r取值很小的时候，窗口sigma_s取值无论如何变化，图像双边滤波效果都不好！
'''

import time
import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/example.png")

start_time = time.time()
dst_edgePreserving = cv.edgePreservingFilter(src)
end_time = time.time()
print("edgePreservingFilter consume times:", end_time - start_time)

start_time = time.time()
dst_bilateral = cv.bilateralFilter(src, 0, 100, 10)
end_time = time.time()
print("bilateralFilter consume times:", end_time - start_time)

start_time = time.time()
dst_pyrMeanShift = cv.pyrMeanShiftFiltering(src, 15, 30)
end_time = time.time()
print("bilateralFilter consume times:", end_time - start_time)


# 可视化
rows = 2
cols = 2
images = [src, dst_edgePreserving, dst_bilateral, dst_pyrMeanShift]
titles = ["original image", "edgePreservingFilter", "bilateralFilter", "pyrMeanShiftFiltering"]
for index, image in enumerate(images):
    plt.subplot(rows, cols, index + 1)
    if index >= len(titles):
        plt.title("image")
    else:
        plt.title(titles[index])
    plt.axis("off")
    plt.imshow(image[:, :, ::-1])
plt.show()