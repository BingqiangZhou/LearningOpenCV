'''
Author       : Bingqiang Zhou
Date         : 2021-02-14 12:22:54
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-14 12:36:55
Description  : 边缘保留滤波算法 – 高斯双边模糊
    前面介绍的图像卷积处理无论是均值还是高斯都是属于模糊卷积，它们都有一个共同的特点就是模糊之后图像的边缘信息不复存在，受到了破坏。
    我们今天介绍的滤波方法有能力通过卷积处理实现图像模糊的同时对图像边缘不会造成破坏，滤波之后的输出完整的保存了图像整体边缘（轮廓）信息，
    我们称这类滤波算法为边缘保留滤波算法（EPF）。最常见的边缘保留滤波算法有以下几种
    -	高斯双边模糊
    -	Meanshift均值迁移模糊
    -	局部均方差模糊
    -	OpenCV中对边缘保留滤波还有一个专门的API
    高斯模糊是考虑图像空间位置对权重的影响，但是它没有考虑图像像素分布对图像卷积输出的影响，
    双边模糊考虑了像素值分布的影响，对像素值空间分布差异较大的进行保留从而完整的保留了图像的边缘信息。
    
    bilateralFilter(
        InputArray 	src,
        OutputArray 	dst,
        int 	d,
        double 	sigmaColor,
        double 	sigmaSpace,
        int 	borderType = BORDER_DEFAULT 
        )
    
    相关资料：https://blog.csdn.net/qq_41498261/article/details/101618119
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/example.png")

dst1 = cv.bilateralFilter(src, 0, 100, 10) # d=0或者负值时，由sigmaSpace计算得来
dst2 = cv.bilateralFilter(src, 5, 100, 10)
dst3 = cv.bilateralFilter(src, 200, 100, 10)

# 可视化
rows = 2
cols = 2
images = [src, dst1, dst2, dst3]
titles = ["original image", "bilateralFilter, d=0", "bilateralFilter, d=5", "bilateralFilter, d=200"]
for index, image in enumerate(images):
    plt.subplot(rows, cols, index + 1)
    if index >= len(titles):
        plt.title("image")
    else:
        plt.title(titles[index])
    plt.axis("off")
    plt.imshow(image[:, :, ::-1])
plt.show()
