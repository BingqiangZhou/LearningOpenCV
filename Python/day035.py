'''
Author       : Bingqiang Zhou
Date         : 2021-02-15 19:52:35
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-15 20:03:42
Description  : USM 锐化增强算法
    图像卷积处理实现锐化有一种常用的算法叫做Unsharpen Mask方法，
    这种锐化的方法就是对原图像先做一个高斯模糊，然后用原来的图像减去一个系数乘以高斯模糊之后的图像，
    然后再把值Scale到0～255的RGB像素值范围之内。
    基于USM锐化的方法可以去除一些细小的干扰细节和噪声，比一般直接使用卷积锐化算子得到的图像锐化结果更加真实可信。

    USM锐化公式表示如下：
    （源图像 – w*高斯模糊）/（1-w）；其中w表示权重（0.1～0.9），默认为0.6

    OpenCV中的代码实现步骤
    1.高斯模糊
    2.权重叠加
    3.输出结果
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/lena.jpg")

# 1.高斯模糊
blured = cv.GaussianBlur(src, ksize=(0, 0), sigmaX=15)

# 2.权重叠加
usm = cv.addWeighted(src, 1.5, blured, -0.5, 0) # dst = src1*alpha + src2*beta + gamma;

# 3.输出结果
# 可视化
rows = 1
cols = 2
images = [src, usm]
titles = ["original image", "usm"]
for index, image in enumerate(images):
    plt.subplot(rows, cols, index + 1)
    if index >= len(titles):
        plt.title("image")
    else:
        plt.title(titles[index])
    plt.axis("off")
    plt.imshow(image[:, :, ::-1])
plt.show()
