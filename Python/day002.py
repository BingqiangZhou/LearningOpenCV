'''
Author       : Bingqiang Zhou
Date         : 2021-01-24 17:31:36
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-01-24 20:06:36
Description  : Day002-图像色彩空间转换
    色彩空间转换函数- cvtColor
    图像保存 - imwrite
'''

import cv2 as cv

src = cv.imread('../data/images/test.png')

if src is not None:
    hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    cv.imwrite('../data/images/test_hsv.png', hsv)
    cv.imshow('day002', hsv)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    print('could not load image')