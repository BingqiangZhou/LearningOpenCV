'''
Author       : Bingqiang Zhou
Date         : 2021-02-15 13:52:49
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-15 14:25:16
Description  : 图像梯度 – 更多梯度算子
    图像的一阶导数算子除了sobel算子之外，常见的还有robert算子与prewitt算子，
    它们也都是非常好的可以检测图像的梯度边缘信息，通过OpenCV中自定义滤波器，
    使用自定义创建的robert与prewitt算子就可以实现图像的rober与prewitt梯度边缘检测，

    robert算子X方向  Y方向 
        -1 0        0 -1
        0 1         1  0

    prewitt算子X方向  Y方向 
    -1 -1 -1        -1 0 +1
     0  0  0        -1 0 +1
    +1 +1 +1        -1 0 +1

    OpenCV中的自定义算子滤波函数如下：

    filter2D(
    InputArray src,
    OutputArray dst,
    int ddepth,
    InputArray 	kernel,
    Point anchor = Point(-1,-1),
    double delta = 0,
    int borderType = BORDER_DEFAULT 
    )

    Python:
    dst	=cv.filter2D(src, ddepth, kernel[, dst[, anchor[, delta[, borderType]]]])

    参考：
        https://blog.csdn.net/zaishuiyifangxym/article/details/89840396
        https://blog.csdn.net/swj110119/article/details/51777422
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

src = cv.imread("../data/images/lena.jpg")

# robert算子
robert_x = np.array([[-1, 0], 
                    [0, 1]]) # x方向
robert_y = np.array([[0, -1], 
                    [1, 0]]) # y方向
dst_robert_x = cv.filter2D(src, ddepth=-1, kernel=robert_x)
dst_robert_y = cv.filter2D(src, ddepth=-1, kernel=robert_y)

dst_robert_x = cv.convertScaleAbs(dst_robert_x)
dst_robert_y = cv.convertScaleAbs(dst_robert_y)

dst_robert_xy = cv.add(dst_robert_x, dst_robert_y, dtype=cv.CV_16S)
dst_robert_xy = cv.convertScaleAbs(dst_robert_xy)

# prewitt算子
prewitt_x = np.array([[-1, -1, -1], 
                        [0, 0, 0], 
                        [1, 1, 1]]) # x方向
prewitt_y = np.array([[-1, 0, 1], 
                        [-1, 0, 1], 
                        [-1, 0, 1]]) # y方向
dst_prewitt_x = cv.filter2D(src, ddepth=-1, kernel=prewitt_x)
dst_prewitt_y = cv.filter2D(src, ddepth=-1, kernel=prewitt_y)

dst_prewitt_x = cv.convertScaleAbs(dst_prewitt_x)
dst_prewitt_y = cv.convertScaleAbs(dst_prewitt_y)

dst_prewitt_xy = cv.add(dst_prewitt_x, dst_prewitt_y, dtype=cv.CV_16S)
dst_prewitt_xy = cv.convertScaleAbs(dst_prewitt_xy)

# 可视化
rows = 2
cols = 4
images = [src, dst_robert_x, dst_robert_y, dst_robert_xy, 
            dst_prewitt_x, dst_prewitt_y, dst_prewitt_xy]
titles = ["original image", "dst_robert_x", "dst_robert_x", "dst_robert_xy",
            "dst_prewitt_x", "dst_prewitt_y", "dst_prewitt_xy"]
for index, image in enumerate(images):
    plt.subplot(rows, cols, index + 1)
    if index >= len(titles):
        plt.title("image")
    else:
        plt.title(titles[index])
    plt.axis("off")
    plt.imshow(image[:, :, ::-1])
plt.show()