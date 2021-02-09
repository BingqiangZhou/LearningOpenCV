'''
Author       : Bingqiang Zhou
Date         : 2021-02-09 17:09:33
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-09 19:08:57
Description  : 图像直方图比较
    图像直方图比较，就是计算两幅图像的直方图数据，比较两组数据的相似性，从而得到两幅图像之间的相似程度，
    直方图比较在早期的CBIR(Content-based image retrieval, 基于内容的图像检索 )中是应用很常见的技术手段，
    通常会结合边缘处理、词袋等技术一起使用。

    OpenCV中直方图比较的API很简单
    compareHist(hist1, hist2, method)
        -常见比较方法有
            相关性：越接近+1越相似，越不相似越接近-1
            卡方： 值越小越相似
            交叉：不太准
            巴氏距离：越接近0则越相似
        具体公式可见：HistCompMethods，https://docs.opencv.org/master/d6/dc7/group__imgproc__hist.html#ga994f53817d621e2e4228fc646342d386
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

m1 = cv.imread("../data/images/m1.png")
m2 = cv.imread("../data/images/m2.png")
g1 = cv.imread("../data/images/cos.jpg")
g2 = cv.imread("../data/images/test.png")

# bgr to hsv,在图像处理中，常常转到HSV色彩空间，并且最常用的通道就是H、S分量
hsv_m1 = cv.cvtColor(m1, cv.COLOR_BGR2HSV)
hsv_m2 = cv.cvtColor(m2, cv.COLOR_BGR2HSV)
hsv_g1 = cv.cvtColor(g1, cv.COLOR_BGR2HSV)
hsv_g2 = cv.cvtColor(g2, cv.COLOR_BGR2HSV)

# 计算H、S通道的直方图，H（0～180）、S（0-256）
hist_m1 = cv.calcHist([hsv_m1], [0, 1], None, [60, 64], [0, 180, 0, 256]) # shape (60, 64)
hist_m2 = cv.calcHist([hsv_m2], [0, 1], None, [60, 64], [0, 180, 0, 256]) # shape (60, 64)
hist_g1 = cv.calcHist([hsv_g1], [0, 1], None, [60, 64], [0, 180, 0, 256]) # shape (60, 64)
hist_g2 = cv.calcHist([hsv_g2], [0, 1], None, [60, 64], [0, 180, 0, 256]) # shape (60, 64)

# 数值归一化，注意确保输入是浮点类型
cv.normalize(hist_m1, hist_m1, 0, 1.0, cv.NORM_MINMAX)
cv.normalize(hist_m2, hist_m2, 0, 1.0, cv.NORM_MINMAX)
cv.normalize(hist_g1, hist_g1, 0, 1.0, cv.NORM_MINMAX)
cv.normalize(hist_g2, hist_g2, 0, 1.0, cv.NORM_MINMAX)

# 直方图比较
methods = {
    "Correlation": cv.HISTCMP_CORREL,                   # 相关性
    "Chi-Square": cv.HISTCMP_CHISQR,                    # 卡方
    "Intersection": cv.HISTCMP_INTERSECT,               # 交叉
    "Bhattacharyya distance": cv.HISTCMP_BHATTACHARYYA  # 巴式距离
    }

for key, method in methods.items():
    v1 = cv.compareHist(hist_m1, hist_m2, method)
    v2 = cv.compareHist(hist_g1, hist_g2, method)
    print("{}:\n v1 {}, v2 {}".format(key, v1, v2))

## 可视化图像
plt.subplot(2, 2, 1)
plt.imshow(m1)
plt.subplot(2, 2, 2)
plt.imshow(m2)
plt.subplot(2, 2, 3)
plt.imshow(g1[:, :, ::-1]) ## 显示rgb图
plt.subplot(2, 2, 4)
plt.imshow(g2[:, :, ::-1])
plt.show()
