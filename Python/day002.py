'''
Author       : Bingqiang Zhou
Date         : 2021-01-24 17:31:36
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-01-24 17:37:22
Description  : 
'''

import cv2 as cv

src = cv.imread('../data/images/test.png')

if src is not None:
    cv.namedWindow('day002', cv.WINDOW_AUTOSIZE)
    hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    cv.imwrite('../data/images/test_hsv.png', hsv)
    cv.imshow('day002', hsv)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    print('could not load image')