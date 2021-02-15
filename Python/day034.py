'''
Author       : Bingqiang Zhou
Date         : 2021-02-15 19:17:35
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-15 19:30:49
Description  : 图像锐化
    图像卷积的主要有三功能分别是图像的模糊/去噪、图像梯度/边缘发现、图像锐化/增强，
    前面的两个功能我们以前通过相关知识点的分享加以了解，学习了相关API的使用。
    图像锐化的本质是图像拉普拉斯滤波加原图权重像素叠加的输出 ：

    -1   -1  -1
    -1    C  -1
    -1    -1 -1
    
    当C值大于8时候表示图像锐化、越接近8表示锐化效果越好
    当C值等于8时候图像的高通滤波
    当C值越大，图像锐化效果在减弱、中心像素的作用在提升
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

src = cv.imread("../data/images/lena.jpg")

# 拉普拉斯算子(八邻域)
# 1, 1, 1
# 1, -8, 1
# 1, 1, 1

# 锐化算子
sharpen_kernel = np.array([[-1, -1, -1], 
                        [-1, 9, -1], 
                        [-1, -1, -1]]) 
dst_sharpen_8 = cv.filter2D(src, ddepth=cv.CV_32F, kernel=sharpen_kernel)

dst_sharpen_8 = cv.convertScaleAbs(dst_sharpen_8)

# 拉普拉斯算子(四邻域)
# 0, 1, 0
# 1, -4, 1
# 0, 1, 0

# 锐化算子
sharpen_kernel = np.array([[0, -1, 0], 
                        [-1, 5, -1], 
                        [0, -1, 0]]) 
dst_sharpen_4 = cv.filter2D(src, ddepth=cv.CV_32F, kernel=sharpen_kernel)

dst_sharpen_4 = cv.convertScaleAbs(dst_sharpen_4)

# 可视化
rows = 1
cols = 3
images = [src, dst_sharpen_4, dst_sharpen_8]
titles = ["original image", "dst_sharpen_4", "dst_sharpen_8"]
for index, image in enumerate(images):
    plt.subplot(rows, cols, index + 1)
    if index >= len(titles):
        plt.title("image")
    else:
        plt.title(titles[index])
    plt.axis("off")
    plt.imshow(image[:, :, ::-1])
plt.show()
