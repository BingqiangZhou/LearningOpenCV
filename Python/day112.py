'''
Author       : Bingqiang Zhou
Date         : 2021-09-01 17:23:45
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-02 13:33:55
Description  : KMeans 图像分割 – 背景替换
    KMeans可以实现简单的证件照片的背景分割提取与替换，大致可以分为如下几步实现
        1. 读入图像建立KMenas样本
        2. 使用KMeans图像分割，指定指定分类数目
        3. 取左上角的label得到背景cluster index
        4. 生成mask区域，然后高斯模糊进行背景替换

    拓展资料：
        官方教程 Understanding K-Means Clustering：https://docs.opencv.org/4.5.3/de/d4d/tutorial_py_kmeans_understanding.html
        官方教程 K-Means Clustering in OpenCV：https://docs.opencv.org/4.5.3/d1/d5c/tutorial_py_kmeans_opencv.html
'''

import cv2 as cv
import numpy as np

# 1. 读入图像建立KMenas样本
img = cv.imread("../data/images/toux.jpg")
data = img.reshape((-1, 3)) # (h*w, 3)
data = np.float32(data) # kmeans输入的数据必须是float32类型
# print(data.shape)

# 2. 使用KMeans图像分割，指定指定分类数目
# kmeans 聚类，最多迭代10次，两次差值小于1则停止
retval, labels, centers = cv.kmeans(data, 4, None, (cv.TermCriteria_MAX_ITER + cv.TermCriteria_EPS, 10, 1), 2, cv.KMEANS_RANDOM_CENTERS)
# print(labels.shape, centers.shape)

# 3. 取左上角的label得到背景cluster index
labels = labels.reshape(img.shape[:2]) # (h, w)
bg_cluster_index = labels[0][0] # 左上角的label

# 4. 生成背景区域mask区域，然后高斯模糊进行背景替换
mask = np.uint8(labels == bg_cluster_index) * 255
# 膨胀操作，让背景边缘向外扩几个像素，便于后续用高斯模糊后的背景mask做权重来处理边缘，让背景替换更加自然
k = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
mask = cv.morphologyEx(mask, cv.MORPH_DILATE, k) 
# 对膨胀后的背景mask进行高斯模糊，作为背景替换的权重，让背景替换的边缘形成渐变，更加自然，而不是看上去是强行加上去的
mask = cv.GaussianBlur(mask, (5, 5), 0)

# 用新的背景颜色合成新的图片
w = (mask / 255.0)[:, :, None] # 大小(h, w, 1)为了与(h, w, 3)做广播
new_bg_color = np.random.randint(0, 256, (1, 1, 3)) # 随机产生颜色，大小(1, 1, 3)为了与(h, w, 3)做广播
img_without_bg = np.uint8(new_bg_color * w + (1.0 - w) * img) # 混合新的背景

# 可视化
cv.imshow("mask", mask)
cv.imshow("img_without_bg", img_without_bg)
cv.waitKey(0)
cv.destroyAllWindows()
