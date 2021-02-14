'''
Author       : Bingqiang Zhou
Date         : 2021-02-14 13:33:17
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-14 14:22:49
Description  : 图像积分图算法
    积分图像是Crow在1984年首次提出，是为了在多尺度透视投影中提高渲染速度，是一种快速计算图像区域和与平方和的算法。
    其核心思想是对每个图像建立自己的积分图查找表，在图像积分处理计算阶段根据预先建立的积分图查找表，
    直接查找从而实现对均值卷积线性时间计算，做到了卷积执行的时间与半径窗口大小的无关联。
    图像积分图在图像特征提取HAAR/SURF、二值图像分析、图像相似相关性NCC计算、图像卷积快速计算等方面均有应用，是图像处理中的经典算法之一。

    图像积分图建立与查找
    在积分图像(Integral Image - ii)上任意位置(x, y)处的ii(x, y)表示该点左上角所有像素之和， 其中(x,y)是图像像素点坐标。

    OpenCV中的相关API如下：
        sum	=	cv.integral(	src[, sum[, sdepth]]	)
        sum, sqsum	=	cv.integral2(	src[, sum[, sqsum[, sdepth[, sqdepth]]]]	)
        sum, sqsum, tilted	=	cv.integral3(	src[, sum[, sqsum[, tilted[, sdepth[, sqdepth]]]]]	)
    官方文档：integral - https://docs.opencv.org/master/d7/d1b/group__imgproc__misc.html#ga97b87bec26908237e8ba0f6e96d23e28
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# 根据和（sum）表计算卷积框内的像素值的和
def get_block_sum(ii, x1, y1, x2, y2, index):
    tl = ii[y1, x1][index]
    tr = ii[y2, x1][index]
    bl = ii[y1, x2][index]
    br = ii[y2, x2][index]
    s = (br - bl - tr + tl)
    return s

# 通过和(sum)表来计算均值模糊
def blur_demo(image, ii, ksize=15):
    h, w, dims = image.shape
    result = np.zeros(image.shape, image.dtype)
    radius = ksize // 2
    for row in range(0, h + radius, 1):
        # 计算左上角（y1）与右下角（y2）的y坐标
        y2 = h if (row + 1)> h else (row + 1)
        y1 = 0 if (row - ksize) < 0 else (row - ksize)
        for col in range(0, w + radius, 1):
            # 计算左上角（x1）与右下角（x2）的x坐标
            x2 = w if (col + 1)>w else (col + 1)
            x1 = 0 if (col - ksize) < 0 else (col - ksize)
            # 计算卷积中心位置
            cx = 0 if (col - radius) < 0 else (col - radius)
            cy = 0 if (row - radius) < 0 else (row - radius)
            # 计算卷积框区域的大小（面积，高乘宽）
            num = (x2 - x1)*(y2 - y1) 
            for i in range(0, 3, 1):
                s = get_block_sum(ii, x1, y1, x2, y2, i) # 获取卷积框区域内像素值的和
                result[cy, cx][i] = s // num # 卷积框区域内像素值的和除以面积则为平均值
    
    return result

src = cv.imread("../data/images/example.png")
sum_table = cv.integral(src) 
# 计算和(sum)表
blur_result = blur_demo(src, sum_table, ksize=15)
# 计算平方和表(sqsum)表
sum_table, sqsum = cv.integral2(src) 
# 计算瓦块和表(tilted)表 \texttt{tilted} (X,Y) = \sum _{y<Y,abs(x-X+1) \leq Y-y-1} \texttt{image} (x,y)
# （0，0）-（x，y）对角线下元素的和作为（x，y）的值
sum_table, sqsum, tilted = cv.integral3(src) 


# 可视化
rows = 1
cols = 2
images = [src, blur_result]
titles = ["original image", "blur use integral"]
for index, image in enumerate(images):
    plt.subplot(rows, cols, index + 1)
    if index >= len(titles):
        plt.title("image")
    else:
        plt.title(titles[index])
    plt.axis("off")
    plt.imshow(image[:, :, ::-1])
plt.show()

