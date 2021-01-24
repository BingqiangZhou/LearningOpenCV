'''
Author       : Bingqiang Zhou
Date         : 2021-01-25 01:12:22
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-01-25 02:05:13
Description  : 图像像素的算术操作
    加add、减subtract、乘multiply、除divide
    防止数据溢出 自行实现clamp，对应C++(saturate_cast<uchar>)
    注意点：图像的数据类型、通道数目、大小必须相同  
'''

import cv2 as cv
import numpy as np


src1 = cv.imread('../data/images/linux_logo.jpg')
src2 = cv.imread('../data/images/windows_logo.jpg')

result = np.zeros_like(src1)

cv.add(src1, src2, result)
# result = cv.add(src1, src2) ## 与上面一行代码等价
cv.imshow("add", result)

cv.subtract(src1, src2, result)
# result = cv.subtract(src1, src2) ## 与上面一行代码等价
cv.imshow("subtract", result)

cv.multiply(src1, src2, result)
# result = cv.multiply(src1, src2) ## 与上面一行代码等价
cv.imshow("multipy", result)

cv.divide(src1, src2, result)
# result = cv.divide(src1, src2) ## 与上面一行代码等价
cv.imshow("divide", result)

def clamp(value):
    if value < 0:
        return 0
    elif value > 255:
        return 255
    return value

def add_implement_by_myself(src1, src2, out=None):
    
    if src1.shape != src2.shape:
        print("shape could not match...\n")
        out = src1
        return out
    
    if out is None:
        out = np.zeros_like(src1)

    ## 防止在相加之后就被截断，先加大存储像素值的字节数
    src1 = np.array(src1, np.uint16)
    src2 = np.array(src2, np.uint16)

    h, w = src1.shape[:2]

    for row in range(h):
        for col in range(w):
            out[row, col] = list(map(clamp, src1[row, col] + src2[row, col]))
    
    return out


add_implement_by_myself(src1, src2, result) 
# result = add_implement_by_myself(src1, src2) ## 与上面一行代码等价
cv.imshow("add_implement_by_myself", result)

cv.waitKey(0)
cv.destroyAllWindows()