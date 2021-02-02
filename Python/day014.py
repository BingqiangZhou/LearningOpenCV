'''
Author       : Bingqiang Zhou
Date         : 2021-02-02 20:46:35
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-02 21:33:38
Description  : 图像插值(Image Interpolation)
    最常见四种插值算法
        INTER_NEAREST = 0
        INTER_LINEAR = 1
        INTER_CUBIC = 2
        INTER_LANCZOS4 = 4
    相关的应用场景
        几何变换、透视变换、插值计算新像素
    resize, 
        如果size有值，使用size做放缩插值，否则根据fx与fy
        另外需要注意的是opencv中的Size是(col, row)即(w, h)
        根据fx与fy的size=(cols * fx, rows * fy)，并向下取整
    相关参考链接：
        几种插值算法对比研究 - https://blog.csdn.net/Trent1985/article/details/45150677
        图像处理之三种常见双立方插值算法 - https://blog.csdn.net/jia20003/article/details/40020775
        图像放缩之双立方插值 - https://blog.csdn.net/jia20003/article/details/6919845
        图像放缩之双线性内插值 - https://blog.csdn.net/jia20003/article/details/6915185
        图像处理之Lanczos采样放缩算法 - https://blog.csdn.net/jia20003/article/details/17856859
'''

import cv2 as cv
import numpy as np

src = cv.imread("../data/images/cos.jpg")
print("source image ", src.shape) # (360, 576, 3)
cv.imshow("source image", src)

h, w = src.shape[:2]

# 最近邻插值方法，resize大小为原图想大小的两倍，需要注意的是opencv中的Size是(col, row)即(w, h)
dst = cv.resize(src, (w * 2, h * 2), interpolation=cv.INTER_NEAREST)
print("INTER_NEAREST ", dst.shape)   # (360, 576, 3)
cv.imshow("INTER_NEAREST", dst)

# 双线性插值方法，resize大小为(500, 500)
dst = cv.resize(src, (500, 500), interpolation=cv.INTER_LINEAR)
print("INTER_LINEAR ", dst.shape) #  (500, 500, 3)
cv.imshow("INTER_LINEAR", dst)

# 双线性三次插值方法（立方卷积插值)，resize为原图大小宽高(列行)的0.5倍（w * 0.5，h * 0.5）(向下取整)
dst = cv.resize(src, (0, 0), fx=0.5, fy=0.5, interpolation=cv.INTER_CUBIC)
print("INTER_CUBIC ", dst.shape) # (180, 288, 3)
cv.imshow("INTER_CUBIC", dst)

# Lanczos插值方法，resize为原图大小（w * 1.5，h * 0.5）,当size有值时，使用size做放缩插值，fx与fy不生效
dst = cv.resize(src, (int(w * 1.5), int(h * 0.5)), fx=1, fy=1, interpolation=cv.INTER_LANCZOS4)
print("INTER_LANCZOS4 ", dst.shape) #  (180, 864, 3)
cv.imshow("INTER_LANCZOS4", dst)

cv.waitKey(0)
cv.destroyAllWindows()