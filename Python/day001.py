'''
Author       : Bingqiang Zhou
Date         : 2021-01-24 17:14:53
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-01-24 17:22:09
Description  : Day01-图像读取与显示
    读取图像 - imread
    显示图像 - imshow
'''

import cv2 as cv

# src = cv.imread('../data/images/test.png')
src = cv.imread('../data/images/test.png', cv.IMREAD_GRAYSCALE)

if src is not None:
    cv.namedWindow('hello, opencv', cv.WINDOW_AUTOSIZE)
    cv.imshow('hello, opencv', src)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    print('could not load image')
