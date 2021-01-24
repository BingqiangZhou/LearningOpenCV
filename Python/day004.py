'''
Author       : Bingqiang Zhou
Date         : 2021-01-24 20:29:34
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-01-24 21:34:15
Description  : Python中的像素遍历与访问
    数组遍历
'''

import cv2 as cv
import numpy as np

# src = cv.imread('../data/images/test.png')
src = cv.imread('../data/images/test.png', cv.IMREAD_GRAYSCALE)

h, w = src.shape[:2]

for i in range(h):
    for j in range(w):
        # if src.ndim == 3: ## rgb
        #     src[i, j, :] = 255 - src[i, j, :]
        #     # src[i, j] = 255 - src[i, j] 这样写也可以，numpy广播机制会把255变成[255, 255. 255]
        # elif src.ndim == 2: ## gray
        #     src[i, j] = 255 - src[i, j]
        
        src[i, j] = 255 - src[i, j]
        
cv.imshow('day004', src)
cv.waitKey(0)
cv.destroyAllWindows()