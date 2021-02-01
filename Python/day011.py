'''
Author       : Bingqiang Zhou
Date         : 2021-02-01 20:04:09
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-01 21:14:18
Description  : 像素归一化
    OpenCV中四种归一化的方法
    - NORM_MINMAX      x = beta + (alpha - beta) * ( (x - min) / (max - min))
    - NORM_INF               x = alpha *  x / max
    - NORM_L1                 x = alpha * x / \sum(|x_i|) 除以L1-范数
    - NORM_L2                 x =  alpha * x / \sqrt(\sum(|x_i^2|)) 除以L2-范数
    最常用的就是NORM_MINMAX归一化方法。

    相关API函数：
    normalize(
    InputArray     src, // 输入图像
    InputOutputArray     dst, // 输出图像
    double     alpha = 1, // NORM_MINMAX时候低值
    double     beta = 0, // NORM_MINMAX时候高值
    int     norm_type = NORM_L2, // 只有alpha
    int     dtype = -1, // 默认类型与src一致
    InputArray     mask = noArray() // mask默认值为空
    )
'''

import cv2 as cv
import numpy as np

src = cv.imread("../data/images/cos.jpg")
cv.imshow("source image", src)
        
# 归一化之前需要将整数类型转换为浮点数类型，不然归一化之后会被截断，值变成0。
src = src.astype(np.float32)
data = np.array([2.0, 8.0, -1.0], dtype=np.float32)

# 初始化存储结果的变量
dst = np.zeros_like(src)
v_dst = np.zeros_like(data)
        
# NORM_L1
cv.normalize(data, v_dst, 1, 0, cv.NORM_L1)
print("NORM_L1: ", v_dst) #  [ 0.18181818  0.72727273 -0.09090909]

cv.normalize(src, dst, 1, 0, cv.NORM_L1)
dst = dst * 5e7 # 归一化之后的值过小，乘以一个合适的值，便于可视化。
cv.imshow("NORM_L1", np.uint8(dst))

# NORM_L2
cv.normalize(data, v_dst, 1, 0, cv.NORM_L2)
print("NORM_L2: ", v_dst) # [ 0.24077171  0.96308684 -0.12038586]

cv.normalize(src, dst, 1, 0, cv.NORM_L2)
print(dst, dst.shape)
dst = dst * 1e5 # 归一化之后的值过小，乘以一个合适的值，便于可视化。
cv.imshow("NORM_L2", np.uint8(dst))

# NORM_INF
cv.normalize(data, v_dst, 1, 0, cv.NORM_INF)
print("NORM_INF", v_dst) # [ 0.25   1.    -0.125]

cv.normalize(src, dst, 1, 0, cv.NORM_INF)
dst = dst * 255 
cv.imshow("NORM_INF", np.uint8(dst))

# NORM_MINMAX
cv.normalize(data, v_dst, 1, 0, cv.NORM_MINMAX)
print("NORM_MINMAX: ", v_dst) # [0.33333334 1.         0.        ]

cv.normalize(src, dst, 1, 0, cv.NORM_MINMAX)
dst = dst * 255
cv.imshow("NORM_MINMAX", np.uint8(dst))

cv.normalize(data, v_dst, 0, 1, cv.NORM_MINMAX) # alpha, beta参数值，那个大那个为alpha，无关顺序
print("NORM_MINMAX", v_dst) # [0.33333334 1.         0.        ]

cv.waitKey(0)
cv.destroyAllWindows()
