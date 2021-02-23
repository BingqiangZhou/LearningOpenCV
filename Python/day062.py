'''
Author       : Bingqiang Zhou
Date         : 2021-02-23 14:29:26
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-23 15:17:57
Description  : 图像形态学 - 膨胀与腐蚀（一）
    膨胀与腐蚀是图像形态学最基础的两个操作，形态学的其它操作都是基于这两个操作基础上得到的，图像形态学是二值图像分析的重要分支学科。
    在OpenCV中膨胀与腐蚀对应两个相关的API，膨胀可以看成是最大值滤波，即用最大值替换中心像素点；
    腐蚀可以看出是最小值滤波，即用最小值替换中心像素点。

    膨胀的API如下：
        void cv::dilate(
        InputArray src,
        OutputArray dst,
        InputArray kernel,
        Point anchor = Point(-1,-1),
        int iterations = 1,
        int borderType = BORDER_CONSTANT,
        const Scalar & borderValue = morphologyDefaultBorderValue() 
        )
    src 输入图像，任意通道的
    dst 输出图像，类型与通道数目必须跟输入保持一致
    kernel 结构元素
    anchor 中心位置锚定
    iterations 循环次数
    borderType 边缘填充类型

    腐蚀的API如下：
        void cv::erode(
        InputArray src,
        OutputArray dst,
        InputArray kernel,
        Point anchor = Point(-1,-1),
        int iterations = 1,
        int borderType = BORDER_CONSTANT,
        const Scalar & borderValue = morphologyDefaultBorderValue() 
        )
    src 输入图像，任意通道的
    dst 输出图像，类型与通道数目必须跟输入保持一致
    kernel 结构元素
    anchor 中心位置锚定
    iterations 循环次数
    borderType 边缘填充类型
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

src = cv.imread("../data/images/dennings.jpg")

kernel = np.ones((3, 3), dtype=np.uint8)
# kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3), (-1, -1))
dilate_dst = cv.dilate(src, kernel)
erode_dst = cv.erode(src, kernel)

# 可视化
rows = 1
cols = 3
images = [src, dilate_dst, erode_dst]
titles = ["original image", "dilate", "erode"]
plt.figure(figsize=(cols * 4, rows * 3)) # Width, height in inches.
for index, image in enumerate(images):
    plt.subplot(rows, cols, index + 1)
    if index >= len(titles):
        plt.title("image")
    else:
        plt.title(titles[index])
    plt.axis("off")
    if image.ndim > 2:
        plt.imshow(image[:, :, ::-1])
    else:
        plt.imshow(image, cmap="gray")
plt.show()
