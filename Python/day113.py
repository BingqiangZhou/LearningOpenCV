'''
Author       : Bingqiang Zhou
Date         : 2021-09-01 18:05:54
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-01 18:42:32
Description  : KMeans 图像分割 – 主色彩提取
    KMeans分割会计算出每个聚类的像素平均值，根据这个可以得到图像的主色彩RGB分布成分多少，
    得到各种色彩在图像中的比重，绘制出图像对应的取色卡！这个方面在纺织与填色方面特别有用！
    主要步骤显示如下：
        1.读入图像建立KMenas样本
        2.使用KMeans图像分割，指定分类数目
        3.统计各个聚类占总像素比率，根据比率建立色卡
    
    拓展资料：
        官方教程 Understanding K-Means Clustering：https://docs.opencv.org/4.5.3/de/d4d/tutorial_py_kmeans_understanding.html
        官方教程 K-Means Clustering in OpenCV：https://docs.opencv.org/4.5.3/d1/d5c/tutorial_py_kmeans_opencv.html
'''

import cv2 as cv
import numpy as np

# 1. 读入图像建立KMenas样本
img = cv.imread("../data/images/master.jpg")
h, w = img.shape[:2]
data = img.reshape((-1, 3)) # (h*w, 3)
data = np.float32(data) # kmeans输入的数据必须是float32类型
# print(data.shape)

# 2. 使用KMeans图像分割，指定指定分类数目
# kmeans 聚类，最多迭代10次，两次差值小于1则停止
retval, labels, centers = cv.kmeans(data, 4, None, (cv.TermCriteria_MAX_ITER + cv.TermCriteria_EPS, 10, 1), 4, cv.KMEANS_PP_CENTERS)
# print(labels.shape, centers.shape)

# 3.统计各个聚类占总像素比率，根据比率建立色卡
index, counts = np.unique(labels, return_counts=True)
rate = counts / (h*w)
# print(index, rate, centers)

# 画出颜色卡
color_card = np.zeros((50, w, 3), dtype=np.uint8)
start = 0
for i, r in enumerate(np.cumsum(rate)): # 累加比例
    end = int(w * r) # w
    # cv.rectangle(color_card, (start, 0, end-start, 50), np.uint8(centers[index[i]]).tolist(), -1)
    # print((start, 0, end-start, 50))
    color_card[:, start:end, :] = np.uint8(centers[index[i]])
    start = end

# 可视化
cv.imshow("image", img)
cv.imshow("image color card", color_card)
cv.waitKey(0)
cv.destroyAllWindows()
