'''
Author       : Bingqiang Zhou
Date         : 2021-08-31 19:00:17
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-31 19:35:16
Description  : HOG特征描述子 – 使用HOG进行对象检测
    对于已经训练好的HOG+SVM的模型，我们可以通过开窗实现对象检测，从而完成自定义对象检测。
    以电表检测为例，这样我们就实现HOG+SVM对象检测全流程。
    OpenCV中实现对每个窗口像素块预测，需要首先加载SVM模型文件，然后使用predict方法实现预测。
    这种方法的缺点就是开窗检测是从左到右、从上到下，是一个高耗时的操作，
    所以步长选择一般会选择HOG窗口默认步长的一半，这样可以减少检测框的数目，
    同时在predict时候会发现多个重复框，求取它们的平均值即可得到最终的检测框。
    拓展资料：
        官方教程：
            OCR of Hand-written Data using SVM：https://docs.opencv.org/4.5.3/dd/d3b/tutorial_py_svm_opencv.html
        官方文档：
            cv::ml::StatModel Class Reference：https://docs.opencv.org/master/db/d7d/classcv_1_1ml_1_1StatModel.html
            cv::ml::SVM Class Reference：https://docs.opencv.org/4.5.3/d1/d2d/classcv_1_1ml_1_1SVM.html
'''

import cv2 as cv
import numpy as np

img = cv.imread("../data/datasets/elec_watch/test/scene_07.jpg")
img = cv.resize(img, (0, 0), fx=0.2, fy=0.2)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
h, w = gray.shape

svm = cv.ml.SVM_load('../data/models/elec_watch_svm.xml')
hog = cv.HOGDescriptor()

mean_x = 0
mean_y = 0
count = 0
for y in range(64, h-64, 4):
    for x in range(32, w-32, 4):
        roi = gray[y-64:y+64, x-32:x+32]
        feature_vector = hog.compute(roi, winStride=(8, 8), padding=(0, 0))
        feature_vector = np.reshape(feature_vector, (1, -1))
        result = svm.predict(feature_vector)[1] # retval, results
        if result[0][0] == 1:
            mean_x += x
            mean_y += y
            count += 1
            print(result, y, x)
            cv.rectangle(img, (x-32, y-64, 64, 128), (0, 127, 0), 2)
            cv.imshow("result", img)
            cv.waitKey(50)


mean_x = mean_x // count
mean_y = mean_y // count
cv.rectangle(img, (mean_x-32, mean_y-64, 64, 128), (0, 0, 255), 2)
cv.imshow("result", img)
cv.waitKey(0)
cv.destroyAllWindows()
