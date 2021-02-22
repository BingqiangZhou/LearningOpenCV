'''
Author       : Bingqiang Zhou
Date         : 2021-02-22 12:23:24
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-22 16:01:02
Description  : 二值图像分析 – 轮廓发现
    图像连通组件分析，可以得到二值图像的每个连通组件，但是我们还无法得知各个组件之间的层次关系与几何拓扑关系，
    如果我们需要进一步分析图像轮廓拓扑信息就可以通过OpenCV的轮廓发现API获取二值图像的轮廓拓扑信息，
    轮廓发现API如下：
        void cv::findContours(
            InputOutputArray image,
            OutputArrayOfArrays contours,
            OutputArray hierarchy,
            int mode,
            int method,
            Point offset = Point() 
        )
    各个参数详解如下：
        Image表示输入图像，必须是二值图像，二值图像可以threshold输出、Canny输出、inRange输出、自适应阈值输出等。
        Contours获取的轮廓，每个轮廓是一系列的点集合
        Hierarchy轮廓的层次信息，每个轮廓有四个相关信息，分别是同层下一个、前一个、第一个子节点、父节点
        mode 表示轮廓寻找时候的拓扑结构返回
            -RETR_EXTERNAL表示只返回最外层轮廓
            -RETR_TREE表示返回轮廓树结构
        Method表示轮廓点集合取得是基于什么算法，常见的是基于CHAIN_APPROX_SIMPLE链式编码方法

    对于得到轮廓，OpenCV通过下面的API绘制每个轮廓
        void cv::drawContours(
            InputOutputArray image,
            InputArrayOfArrays contours,
            int contourIdx,
            const Scalar & 	color,
            int thickness = 1,
            int lineType = LINE_8,
            InputArray 	hierarchy = noArray(),
            int maxLevel = INT_MAX,
            Point offset = Point() 
        )
    当thickness为正数的时候表示绘制该轮廓
    当thickness为-1表示填充该轮廓
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/coins.jpg")

# 去噪声+二值化
blured = cv.GaussianBlur(src, (3, 3), 0)
gray = cv.cvtColor(blured, cv.COLOR_BGR2GRAY)
thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)

# 边缘检测
canny = cv.Canny(src, 0, 255)


temp = src.copy()
# 发现轮廓
contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) # 只获取最上层轮廓
# print(hierarchy, hierarchy.shape)
# print(len(contours))
for c in range(len(contours)):
    # 绘制轮廓，每次画轮廓中的第c个
    cv.drawContours(src, contours, c, (0, 0, 255), 2, cv.LINE_8)
    # cv.drawContours(src, contours, c, (0, 0, 255), cv.FILLED, cv.LINE_8)
    
    # 绘制最上层（没有父节点）的轮廓
    # hierarchy包含索引信息：同层下一个、前一个、第一个子节点、父节点
    if hierarchy[0][c][3] == -1:
        cv.drawContours(temp, contours, c, (0, 0, 255), 2, cv.LINE_8)


# 可视化 
rows = 2
cols = 2
images = [src, binary, canny, temp]
titles = ["dst image", "binary image", "canny", "hierarchy index=-1"]
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
