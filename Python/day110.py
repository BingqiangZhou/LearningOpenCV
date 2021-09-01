'''
Author       : Bingqiang Zhou
Date         : 2021-09-01 16:24:46
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-01 16:48:07
Description  : KMeans 数据分类
    K-Means算法的作者是MacQueen， K-Means的算法是对数据进行分类的算法，采用的硬分类方式，是属于非监督学习的算法，
    预先要求知道分为几个类别，然后每个类别有一个中心点，根据距离度量来决定每个数据点属于哪个类别标签，
    一次循环实现对所有数据点分类之后，会根据标签重新计算各个类型的中心位置，
    然后继续循环数据集再次分类标签样本数据，如此不断迭代，直到指定的循环数目或者前后两次delta小于指定阈值，
    停止计算，得到最终各个样本数据的标签。
 
    OpenCV中KMeans数据分类的API为：
    double cv::kmeans(
        InputArray data,
        int K,
        InputOutputArray bestLabels,
        TermCriteria criteria,
        int attempts,
        int flags,
        OutputArray centers = noArray() 
    )
    data表示输入的样本数据，必须是按行组织样本，每一行为一个样本数据，列表示样本的维度
    K表示最终的分类数目
    bestLabels 表示最终分类每个样本的标签
    criteria 表示KMeans分割的停止条件
    attempts 表示采样不同初始化标签尝试次数
    flag表示中心初始化方法
    -	KMEANS_RANDOM_CENTERS 	
    -	KMEANS_PP_CENTERS 	
    -	KMEANS_USE_INITIAL_LABELS
    centers表示最终分割以后的每个cluster的中心位置

    拓展资料：
        官方教程 Understanding K-Means Clustering：https://docs.opencv.org/4.5.3/de/d4d/tutorial_py_kmeans_understanding.html
        官方教程 K-Means Clustering in OpenCV：https://docs.opencv.org/4.5.3/d1/d5c/tutorial_py_kmeans_opencv.html
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

c1 = np.random.randint(0, 50, (100, 2)) # 第一簇
c2 = np.random.randint(51, 100, (100, 2)) # 第二簇
data = np.vstack([c1, c2]) # (200, 2)
data = np.float32(data) # kmeans输入的数据必须是float32类型
# print(data.shape)

# kmeans 聚类，最多迭代10次，两次差值小于1则停止
retval, labels, centers = cv.kmeans(data, 2, None, (cv.TermCriteria_MAX_ITER + cv.TermCriteria_EPS, 10, 1), 2, cv.KMEANS_RANDOM_CENTERS)
# print(labels.shape, centers.shape)

# 给数据打上聚类后的标签
A = data[labels[:, 0] == 0]
B = data[labels[:, 0] == 1]

plt.scatter(A[:, 0], A[:, 1], c='b') # 画出第一簇
plt.scatter(B[:, 0], B[:, 1], c='g') # 画出第二簇
plt.scatter(centers[:, 0], centers[:, 1], c='r') # 画出簇中心点
plt.show()