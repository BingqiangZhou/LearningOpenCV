'''
Author       : Bingqiang Zhou
Date         : 2021-02-17 22:17:38
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-17 22:57:37
Description  : 二值图像连通组件状态统计
    OpenCV中的连通组件标记算法有两个相关的API，
    一个是不带统计信息的API
        int cv::connectedComponents(
        InputArray 	image, // 输入二值图像，黑色背景
        OutputArray 	labels, // 输出的标记图像，背景index=0
        int 	connectivity = 8, // 连通域，默认是8连通
        int 	ltype = CV_32S // 输出的labels类型，默认是CV_32S
        )
    另外一个是会输出连通组件统计信息的相关API，
        int cv::connectedComponentsWithStats(
        InputArray image,
        OutputArray labels,
        OutputArray stats,
        OutputArray centroids,
        int connectivity,
        int ltype,
        int ccltype 
        )
    相关的统计信息包括在输出stats的对象中，每个连通组件有一个这样的输出结构体。
    CC_STAT_LEFT 连通组件外接矩形左上角坐标的X位置信息

    CC_STAT_TOP 连通组件外接左上角坐标的Y位置信息

    CC_STAT_WIDTH 连通组件外接矩形宽度

    CC_STAT_HEIGHT 连通组件外接矩形高度

    CC_STAT_AREA 连通组件的面积大小，基于像素多少统计

    Centroids输出的是每个连通组件的中心位置坐标(x, y)
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

src = cv.imread("../data/images/rice.png")

blured = cv.GaussianBlur(src, (3, 3), 0) # 高斯模糊
gray = cv.cvtColor(blured, cv.COLOR_BGR2GRAY) # 转换为灰度图

thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU) # 转换为二值图

# nums_label, labels = cv.connectedComponents(binary, connectivity=8, ltype=cv.CV_32S) # 二值图像联通组件寻找
nums_label, labels, stats, centroids = cv.connectedComponentsWithStats(binary) # 带状态的二值图像联通组件寻找

print("the number of rice: ", nums_label - 1) # 去掉背景
# print("left-x\t left-y\t height\t width\t area\n", stats)

# 在图像中画出联通组件的中心以及外接矩形框
for i, data in enumerate(zip(stats, centroids)):
    if i == 0: # 跳过背景
        continue
    x, y, w, h, s = data[0] # 将组件状态：左上角x坐标、左上角y坐标、宽、高、面积
    cx, cy = data[1]        # 将组件中心：x坐标、y坐标
    cv.rectangle(src, (x, y), (x + w, y + h), (0, 0, 255))
    cv.circle(src, (int(cx), int(cy)), 4, (0, 0, 255), thickness=cv.FILLED)

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