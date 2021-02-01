'''
Author       : Bingqiang Zhou
Date         : 2021-02-01 11:18:31
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-01 11:32:50
Description  : 图像像素值统计
    像素值统计
    - 最小(min)
    - 最大(max)
    - 均值(mean)
    - 标准方差(standard deviation)

    API
    - 最大最小值minMaxLoc
    - 计算均值与标准方差meanStdDev
'''

import cv2 as cv
import numpy as np

src = cv.imread("../data/images/cos.jpg")
cv.imshow("source image", src)
        
# 最大最小值minMaxLoc
# 需要注意的是，只能在单通道上操作
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(gray)
print("minVal: {}, maxVal: {}".format(min_val, max_val))
print("minVal loc: , maxVal loc: {}".format(min_loc, max_loc))
        
# 计算均值与标准方差meanStdDev
mean, stddev = cv.meanStdDev(src)
print("mean: ", mean)
print("stddev: ", stddev)
        
# 如果当前通道的值大于当前通道的均值，则赋为255，否则为0（已初始化为0）
dst = np.zeros_like(src)
for channel in range(dst.shape[2]):
    dst[src[:,:, channel] > mean[channel]] = 255

cv.imshow("dst", dst)

cv.waitKey(0)
cv.destroyAllWindows()