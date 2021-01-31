'''
Author       : Bingqiang Zhou
Date         : 2021-01-31 19:33:10
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-01-31 19:39:13
Description  : 图像像素的逻辑操作
    - bitwise_and 与
    - bitwise_xor 异或
    - bitwise_or  或
    上面三个类似，都是针对两张图像的位操作

    - bitwise_not 非
    针对输入图像, 图像取反操作，二值图像分析中经常用
'''

import cv2 as cv
import numpy as np

m1 = np.zeros([400, 400, 3], dtype=np.uint8)
m2 = np.zeros([400, 400, 3], dtype=np.uint8)

m1[100:200,100:200,:] = [0, 0, 255] # 红色
m2[150:250,150:250,:] = [0, 255, 255] # 黄色

# 与
dst = cv.bitwise_and(m1, m2)
cv.imshow('bitwise_and', dst)

# 或
dst = cv.bitwise_or(m1, m2)
cv.imshow("bitwise_or", dst)

# 异或
dst = cv.bitwise_xor(m1, m2)
cv.imshow("bitwise_xor", dst)

# 非
dst = cv.bitwise_not(m1)
cv.imshow("bitwise_not", dst)

src = cv.imread('../data/images/cos.jpg')
dst = cv.bitwise_not(src)
cv.imshow("src bitwise_not", dst)


cv.waitKey(0)
cv.destroyAllWindows()

