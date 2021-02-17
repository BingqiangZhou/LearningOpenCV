'''
Author       : Bingqiang Zhou
Date         : 2021-02-17 20:58:36
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-17 22:11:24
Description  : 二值图像 联通组件寻找
    连通组件标记算法介绍
    连接组件标记算法(connected component labeling algorithm)是图像分析中最常用的算法之一，
    算法的实质是扫描二值图像的每个像素点，对于像素值相同的而且相互连通分为相同的组(group)，最终得到图像中所有的像素连通组件。
    扫描的方式可以是从上到下，从左到右，对于一幅有N个像素的图像来说，最大连通组件个数为N/2。
    扫描是基于每个像素单位，OpenCV中进行连通组件扫码调用的时候必须保证背景像素是黑色、前景像素是白色。
    
    最常见的连通组件扫码有如下两类算法：
        1. 基于图的搜索算法（一步法）
        2. 基于扫描、等价类合并算法（两步法）

    OpenCV中支持连通组件扫描的API有两个，一个是带统计信息一个不带统计信息。
    不带统计信息的API及其解释如下：
    int cv::connectedComponents(
    InputArray 	image, // 输入二值图像，黑色背景
    OutputArray 	labels, // 输出的标记图像，背景index=0
    int 	connectivity = 8, // 连通域，默认是8连通
    int 	ltype = CV_32S // 输出的labels类型，默认是CV_32S
    )
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

src = cv.imread("../data/images/rice.png")

blured = cv.GaussianBlur(src, (3, 3), 0) # 高斯模糊
gray = cv.cvtColor(blured, cv.COLOR_BGR2GRAY) # 转换为灰度图

thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU) # 转换为二值图

nums_label, labels = cv.connectedComponents(binary, connectivity=8, ltype=cv.CV_32S) # 二值图像联通组件寻找
print("the number of rice: ", nums_label - 1) # 去掉背景

# 将不同的label应用不同的颜色
temp = np.zeros_like(labels)
cv.normalize(labels, temp, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
labels = cv.convertScaleAbs(temp)
# print(np.unique(labels))
colored_labels = cv.applyColorMap(labels, cv.COLORMAP_HOT)

# 可视化
rows = 1
cols = 2
images = [src, colored_labels]
titles = ["original image", "colored_labels"]
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

