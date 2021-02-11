'''
Author       : Bingqiang Zhou
Date         : 2021-02-08 21:52:55
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-11 14:30:02
Description  : 图像直方图
    图像直方图的解释
    图像直方图是图像像素值的统计学特征、计算代价较小，具有图像平移、旋转、缩放不变性等众多优点，
    广泛地应用于图像处理的各个领域，特别是灰度图像的阈值分割、基于颜色的图像检索以及图像分类、反向投影跟踪。
    常见的分为灰度直方图、颜色直方图

    Bins是指直方图的大小范围， 对于像素值取值在0～255之间的，最少有256个bin，此外还可以有16、32、48、128等，256除以bin的大小应该是整数倍。

    OpenCV中相关API
    hist = cv.calcHist(images, channels, mask, histSize, ranges[, hist[, accumulate]])
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def custom_clacHist(image, bins=256, show_fig=True):
    h, w, c = image.shape
    num_color_per_bin = 256 // bins
    colormap = ['blue', 'green', 'red', 'gray']

    hist = np.zeros([bins, c], dtype=np.uint)
    for i in range(c):
        for row in range(h):
            for col in range(w):
                v = image[row, col, i] # value of color in [0, 255]
                hist[v // num_color_per_bin, i] += 1
        # hist = cv.calcHist([src], [i], None, [bins], [0, 256])
    
    # show figure
    if show_fig is True:
        for i in range(c):
            plt.plot(hist[:, i], color=colormap[i], label=colormap[i] if colormap[i] is not 'gray' else 'alpha')
        plt.legend()
        plt.show()
    
    return hist

src = cv.imread("../data/images/cos.jpg")
# src = cv.cvtColor(src, cv.COLOR_BGR2RGBA)
cv.imshow("source image", src)

# 灰度直方图
# calcHist: (images, channels, mask, histSize, ranges, hist=..., accumulate=...)
hist = cv.calcHist([src], [0], None, [256], [0, 256])
x = list(range(0, 256))
plt.bar(x, hist[:, 0])
plt.show()

# 颜色直方图
hist1 = cv.calcHist([src], [0], None, [256], [0, 256])
hist2 = cv.calcHist([src], [1], None, [256], [0, 256])
hist3 = cv.calcHist([src], [2], None, [256], [0, 256])
plt.plot(hist1[:, 0], color='b', label='b')
plt.plot(hist2[:, 0], color='g', label='g')
plt.plot(hist3[:, 0], color='r', label='r')
plt.legend()
plt.show()

custom_clacHist(src, bins=256)
custom_clacHist(src, bins=64)

cv.waitKey(0)
cv.destroyAllWindows()
