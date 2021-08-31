'''
Author       : Bingqiang Zhou
Date         : 2021-08-31 12:12:20
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-31 12:37:19
Description  : HOG特征与行人检测
    HOG(Histogram of Oriented Gradient)特征在对象识别与模式匹配中是一种常见的特征提取算法，
    是基于本地像素块进行特征直方图提取的一种算法，对象局部的变形与光照影响有很好的稳定性，
    最初是用HOG特征来来识别人像，通过HOG特征提取+SVM训练，可以得到很好的效果。
    
    拓展资料：
        HOG特征：https://zhuanlan.zhihu.com/p/40960756
        传统目标检测之HOG特征：https://zhuanlan.zhihu.com/p/75538637
        官方文档：https://docs.opencv.org/4.5.3/d5/d33/structcv_1_1HOGDescriptor.html
'''

import cv2 as cv

img = cv.imread("../data/images/pedestrian.png")

# 初始化
hog = cv.HOGDescriptor()
# 设置默认的行人SVM检测器
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
# 检测行人
(rects, weights) = hog.detectMultiScale(img, winStride=(4, 4), padding=(8, 8), scale=1.25, useMeanshiftGrouping=False)
# print(rects, weights)

# 可视化
for r in rects:
    cv.rectangle(img, r, (0, 255, 0), 2)

cv.imshow("result", img)
cv.waitKey(0)
cv.destroyAllWindows()
