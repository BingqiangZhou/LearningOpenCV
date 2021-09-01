'''
Author       : Bingqiang Zhou
Date         : 2021-09-02 00:07:21
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-02 00:32:15
Description  : KNN算法使用
    OpenCV中机器学习模块的最近邻算法KNN， 对使用KNN训练好的XML文件，可以通过算法接口的load方法加载成为KNN分类器，使用findNearest方法进行预测。OpenCV KNN预测方法参数解释如下：
    virtual float cv::ml::KNearest::findNearest(
        InputArray 	samples,
        int 	k,
        OutputArray 	results,
        OutputArray 	neighborResponses = noArray(),
        OutputArray 	dist = noArray() 
    )
    其中sample是待预测的数据样本
    K表示选择最近邻的数目
    Result表示预测结果
    neighborResponses表示每个样本的前k个邻居
    dist表示每个样本前k的邻居的距离

    拓展资料：
        官方教程：
            Understanding k-Nearest Neighbour：https://docs.opencv.org/4.5.3/d5/d26/tutorial_py_knn_understanding.html
            OCR of Hand-written Data using kNN：https://docs.opencv.org/4.5.3/d8/d4b/tutorial_py_knn_opencv.html
        官方API文档：
            cv::ml::KNearest Class Reference：https://docs.opencv.org/4.5.3/dd/de1/classcv_1_1ml_1_1KNearest.html
'''

import cv2 as cv
import numpy as np

knn = cv.ml.KNearest_load("../data/models/digit_knn.xml")

def predict(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    test = cv.resize(gray, (20, 20)).reshape(1, -1).astype(np.float32)
    ret, result, neighbours, dist = knn.findNearest(test, k=5)
    return int(result[0][0])


img1 = cv.imread("../data/images/knn_01.png") # label 1
result1 = predict(img1)
cv.imshow("knn_01", img1)
print(f"knn predict {result1}, actual label 1")


img2 = cv.imread("../data/images/knn_02.png") # label 2
result2 = predict(img2)
cv.imshow("knn_02", img2)
print(f"knn predict {result2}, actual label 2")

cv.waitKey(0)
cv.destroyAllWindows()