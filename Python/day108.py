'''
Author       : Bingqiang Zhou
Date         : 2021-09-01 10:44:31
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-01 10:55:15
Description  : 特征提取之关键点检测 - GFTTDetector
    该方法是基于shi-tomas角点检测变化而来的一种特征提取方法，OpenCV创建该检测器的API与goodfeaturetotrack的API参数极其类似：
    Ptr<GFTTDetector> cv::GFTTDetector::create(
        int maxCorners = 1000,
        double qualityLevel = 0.01,
        double minDistance = 1,
        int blockSize = 3,
        bool useHarrisDetector = false,
        double k = 0.04 
    )
    唯一不同的，该方法返回一个指针。

    PS:
    需要注意的是该方法无法提取描述子，只支持提取关键点！
'''

import cv2 as cv

img = cv.imread("../data/images/test1.png")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

gftt = cv.GFTTDetector_create()
keypoints = gftt.detect(gray, None)

img = cv.drawKeypoints(img, keypoints, None)
cv.imshow("result", img)

cv.waitKey(0)
cv.destroyAllWindows()
