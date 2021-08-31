'''
Author       : Bingqiang Zhou
Date         : 2021-08-31 13:00:21
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-31 13:05:02
Description  : HOG特征描述子 – 多尺度检测
    HOG(Histogram of Oriented Gradient)特征本身不支持旋转不变性，通过金字塔可以支持多尺度检测实现尺度空间不变性，OpenCV中支持HOG描述子多尺度检测的相关API如下：
    virtual void cv::HOGDescriptor::detectMultiScale(
        InputArray 	img,
        std::vector&lt; Rect &gt; & 	foundLocations,
        double 	hitThreshold = 0,
        Size 	winStride = Size(),
        Size 	padding = Size(),
        double 	scale = 1.05,
        double 	finalThreshold = 2.0,
        bool 	useMeanshiftGrouping = false 
    )
    Img表示输入图像
    foundLocations表示发现对象矩形框
    hitThreshold表示SVM距离度量，默认0表示，表示特征与SVM分类超平面之间
    winStride表示窗口步长
    padding表示填充
    scale表示尺度空间
    finalThreshold 最终阈值，默认为2.0
    useMeanshiftGrouping 不建议使用，速度太慢拉

    这个其中窗口步长与Scale对结果影响最大，特别是Scale，小的尺度变化有利于检出低分辨率对象，
    同事也会导致FP（false  positive，将背景检测为对象）发生，高的可以避免FP但是会产生FN（false negative，有对象漏检）。
    窗口步长是一个或者多个block区域。
'''

import cv2 as cv

img = cv.imread("../data/images/pedestrian_02.png")

# 初始化
hog = cv.HOGDescriptor()
# 设置默认的行人SVM检测器
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

# 检测行人 scale 1.05，有出现false  positive的情况
result1 = img.copy()
(rects, weights) = hog.detectMultiScale(img, winStride=(4, 4), padding=(8, 8), scale=1.05, useMeanshiftGrouping=False)
for r in rects:
    cv.rectangle(result1, r, (0, 255, 0), 2) 
cv.imshow("result-scale 1.05", result1) 

# 检测行人 scale 1.25
result2 = img.copy()
(rects, weights) = hog.detectMultiScale(img, winStride=(4, 4), padding=(8, 8), scale=1.25, useMeanshiftGrouping=False)
for r in rects:
    cv.rectangle(result2, r, (0, 255, 0), 2)
cv.imshow("result-scale 1.25", result2)

cv.waitKey(0)
cv.destroyAllWindows()
