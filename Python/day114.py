'''
Author       : Bingqiang Zhou
Date         : 2021-09-01 23:03:25
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-02 00:13:00
Description  : KNN算法介绍
    OpenCV中机器学习模块的最近邻算法KNN，使用KNN算法实现手写数字识别，
    OpenCV在sample/data中有一张自带的手写数字数据集图像，0~9 每个有500个样本，总计有5000个数字。
    图像大小为1000x2000的大小图像，分割为20x20大小的单个数字图像，每个样本400个像素。
    然后使用KNN相关API实现训练与结果的保存。
    大致的顺序如下：
        1. 读入测试图像digit.png(可以在我的github下载，不知道地址看置顶帖子)
        2. 构建样本数据与标签
        3. 创建KNN训练并保存训练结果
    
    拓展资料：
        官方教程：
            Understanding k-Nearest Neighbour：https://docs.opencv.org/4.5.3/d5/d26/tutorial_py_knn_understanding.html
            OCR of Hand-written Data using kNN：https://docs.opencv.org/4.5.3/d8/d4b/tutorial_py_knn_opencv.html
        官方API文档：
            cv::ml::KNearest Class Reference：https://docs.opencv.org/4.5.3/dd/de1/classcv_1_1ml_1_1KNearest.html
'''

import cv2 as cv
import numpy as np

# 图像一行有100个数字图像，每个数有500个，并且按数字顺序排列，即前五行为0，后面依次1-9。
img = cv.imread("../data/datasets/digits/digits.png")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 先将图像切分50行，再将每一行分别切成100列 # (50 x 100 x 20 x 20)
data = np.array([ np.hsplit(row, 100) for row in np.vsplit(gray, 50) ])

# 切分训练集以及测试集 8:2
train_data = data[:, :80].reshape((-1, 400)).astype(np.float32) # (4000, 400)
test_data = data[:, 80:].reshape((-1, 400)).astype(np.float32) # (1000, 400)
train_labels = np.vstack([ np.full((400, 1), i) for i in range(10)]) # (4000, 1)
test_labels = np.vstack([ np.full((100, 1), i) for i in range(10)]) # (1000, 1)

# 创建KNN训练并保存训练结果
knn = cv.ml.KNearest_create()
knn.train(train_data, cv.ml.ROW_SAMPLE, train_labels)
knn.save("../data/models/digit_knn.xml")

# 对测试集数据进行预测，计算正确率
ret, result, neighbours, dist = knn.findNearest(test_data, k=5)
matches = (result == test_labels).astype(np.uint8)
accuracy = np.count_nonzero(matches) / result.size
print("accuracy for test set: ", accuracy)