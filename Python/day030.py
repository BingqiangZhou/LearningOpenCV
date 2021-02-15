'''
Author       : Bingqiang Zhou
Date         : 2021-02-15 10:25:55
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-15 13:03:13
Description  : OpenCV中的自定义滤波器
    图像卷积最主要功能有图像模糊、锐化、梯度边缘等，前面已经分享图像卷积模糊的相关知识点，
    OpenCV除了支持上述的卷积模糊（均值与边缘保留）还支持自定义卷积核，实现自定义的滤波操作。
    自定义卷积核常见的主要是均值、锐化、梯度等算子。下面的三个自定义卷积核分别可以实现卷积的均值模糊、锐化、梯度功能。

    1，	1， 1      0， -1， 0        1， 0
    1，	1， 1      -1， 5， -1        0  -1
    1，	1， 1      0， -1， 0 

    OpenCV自定义滤波器API:
        dst=cv.filter2D(src, ddepth, kernel[, dst[, anchor[, delta[, borderType]]]]	)

    int ddepth, // 默认-1，表示输入与输出图像类型一致，但是当涉及浮点数计算时候，需要设置为CV_32F。
    滤波完成之后需要使用convertScaleAbs函数将结果转换为字节（uchar）类型。
    convertScaleAbs函数
        dst	=	cv.convertScaleAbs(	src[, dst[, alpha[, beta]]]	)
        \texttt{dst} (I)= \texttt{saturate\_cast<uchar>} (| \texttt{src} (I)* \texttt{alpha} + \texttt{beta} |)
    convertScaleAbs函数为 abs(src*alpha+beta) 再通过saturate_cast函数转换到0-255
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

src = cv.imread("../data/images/lena.jpg")

# 均值模糊 等效于 dst = cv.blur(src, (15, 15))
# kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 9
kernel = np.ones((15, 15)) / 225
dst_blur = cv.filter2D(src, ddepth=-1, kernel=kernel)

# 锐化
kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
dst_sharpen = cv.filter2D(src, ddepth=-1, kernel=kernel)

# 梯度边缘
kernel = np.array([[0, -1], [1, 0]])
# dst_gradient_edge = cv.filter2D(src, ddepth=-1, kernel=kernel)
dst_gradient_edge = cv.filter2D(src, ddepth=cv.CV_32F, kernel=kernel)
dst_gradient_edge = cv.convertScaleAbs(dst_gradient_edge) # 将结果转换为uchar类型（0-255）

# 可视化
rows = 2
cols = 2
images = [src, dst_blur, dst_sharpen, dst_gradient_edge]
titles = ["original image", "blur", "sharpen", "gradient_edge"]
for index, image in enumerate(images):
    plt.subplot(rows, cols, index + 1)
    if index >= len(titles):
        plt.title("image")
    else:
        plt.title(titles[index])
    plt.axis("off")
    plt.imshow(image[:, :, ::-1])
plt.show()