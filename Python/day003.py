'''
Author       : Bingqiang Zhou
Date         : 2021-01-24 18:42:19
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-01-24 20:07:58
Description  : 图像对象的创建与赋值
    Python中Numpy数组对象 - copy, zeros, ones, eye 
'''

import cv2 as cv
import numpy as np


src = cv.imread('../data/images/test.png')

## 复制（克隆）
m1 = np.copy(src)

## 赋值
m2 = src

src[100:200, 200:300, :] = 250
# cv.imshow("m2", m2)

m3 = np.zeros([512, 512], np.uint8)
# cv.imshow("m3", m3)

m4 = np.zeros(src.shape, src.dtype)
# cv.imshow("m4", m4)

m5 = np.ones(src.shape, src.dtype)
# cv.imshow("m5", m5)

m6 = np.eye(100, dtype=np.uint16)
cv.imshow("m6", m6)

cv.waitKey(0)
cv.destroyAllWindows()