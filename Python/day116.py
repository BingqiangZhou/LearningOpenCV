'''
Author       : Bingqiang Zhou
Date         : 2021-09-02 11:59:39
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-02 12:12:40
Description  : 决策树算法 介绍与使用
    OpenCV中机器学习模块的决策树算法分为两个类别，
    一个是随机森林(Random Trees)、另外一个强化分类(Boosting Classification)。
    这两个算法都属于决策树算法。
    virtual float cv::ml::StatModel::predict(
        InputArray 	samples,
        OutputArray results = noArray(),
        int flags = 0 
    )const
    sample输入样本
    result预测结果

    拓展资料：
        官方文档：
            cv::ml::StatModel Class Reference：https://docs.opencv.org/4.5.3/db/d7d/classcv_1_1ml_1_1StatModel.html
            cv::ml::DTrees Class Reference：https://docs.opencv.org/4.5.3/d8/d89/classcv_1_1ml_1_1DTrees.html
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

# 创建随机森林(Random Trees)并保存训练结果
rt = cv.ml.RTrees_create()
rt.train(train_data, cv.ml.ROW_SAMPLE, train_labels)
# rt.save("../data/models/digit_rtrees.xml")
# 对测试集数据进行预测，计算正确率
# rt = cv.ml.RTrees_load("../data/models/digit_rtrees.xml")
ret, result = rt.predict(test_data)
matches = (result == test_labels).astype(np.uint8)
accuracy = np.count_nonzero(matches) / result.size
print("RTrees: accuracy for test set: ", accuracy)

# 创建强化分类(Boosting Classification)并保存训练结果
boost = cv.ml.Boost_create()
boost.train(train_data, cv.ml.ROW_SAMPLE, train_labels)
# boost.save("../data/models/digit_dt_boost.xml")
# 对测试集数据进行预测，计算正确率
# boost = cv.ml.Boost_load("../data/models/digit_dt_boost.xml")
ret, result = boost.predict(test_data)
matches = (result == test_labels).astype(np.uint8)
accuracy = np.count_nonzero(matches) / result.size
print("Boost: accuracy for test set: ", accuracy)