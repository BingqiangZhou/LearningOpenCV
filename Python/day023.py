'''
Author       : Bingqiang Zhou
Date         : 2021-02-10 21:55:35
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-10 22:05:15
Description  : 图像中值模糊
    中值滤波本质上是统计排序滤波器的一种，中值滤波对图像特定噪声类型（椒盐噪声）会取得比较好的去噪效果，也是常见的图像去噪声与增强的方法之一。
    中值滤波也是窗口在图像上移动，其覆盖的对应ROI区域下，所有像素值排序，取中值作为中心像素点的输出值

    OpenCV中值滤波API函数如下：
        dst = cv.medianBlur(src, ksize[, dst])
        其中ksize必须是奇数，而且必须大于1
'''

import cv2 as cv
import matplotlib.pyplot as plt

# 带有椒盐噪声的图片
src = cv.imread("../data/images/sp_noise.png")

# 中值模糊
dst = cv.medianBlur(src, 5)

# 可视化
rows = 1
cols = 2
plt.subplot(rows, cols, 1)
plt.title("src")
plt.axis("off")
plt.imshow(src[:, :, ::-1])

plt.subplot(rows, cols, 2)
plt.title("medianBlur 5")
plt.axis("off")
plt.imshow(dst[:, :, ::-1])
plt.show()