'''
Author       : Bingqiang Zhou
Date         : 2021-02-17 15:35:51
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-17 15:51:41
Description  : OpenCV中的基本阈值操作
    假设我们已经寻找到合适的阈值T，那么对图像二值化分割可以看成是一种基本的阈值化操作，
    其实OpenCV除了支持正常的二值化阈值分割操作之外，还支持一些其它的阈值操作，OpenCV中支持的阈值操作的API如下：
    double cv::threshold(
    InputArray src,
    OutputArray dst,
    double thresh,
    double maxval,
    int type
    )
    其中type表示阈值分割的方法，支持如下五种：
    THRESH_BINARY = 0       二值分割，如果值大于thresh，则为maxval否则为0
    THRESH_BINARY_INV = 1   反向二值分割，如果值大于thresh，则为0否则为maxval
    THRESH_TRUNC = 2        截断，如果值大于thresh，则为thresh，否则为原来的值
    THRESH_TOZERO = 3       取零，如果值大于thresh，则为原来的值，否则为0
    THRESH_TOZERO_INV = 4   反向取零，如果值大于thresh，则为0，否则为原来的值
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/lena.jpg")
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

methods = [cv.THRESH_BINARY, cv.THRESH_BINARY_INV, cv.THRESH_TRUNC, cv.THRESH_TOZERO, cv.THRESH_TOZERO_INV]
names = ["THRESH_BINARY", "THRESH_BINARY_INV", "THRESH_TRUNC", "THRESH_TOZERO", "THRESH_TOZERO_INV"]

t = 127
dsts = []
for method in methods:
    threshold, binary = cv.threshold(gray, t, 255, method)
    dsts.append(binary)

# 可视化
rows = 2
cols = 3
images = [src]
images.extend(dsts)
titles = ["original image"]
titles.extend(names)
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
