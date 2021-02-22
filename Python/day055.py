'''
Author       : Bingqiang Zhou
Date         : 2021-02-22 17:54:35
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-22 18:21:43
Description  : 二值图像分析 – 凸包检测
    对二值图像进行轮廓分析之后，对获取到的每个轮廓数据，
    可以构建每个轮廓的凸包，构建完成之后会返回该凸包包含的点集。
    根据返回的凸包点集可以绘制该轮廓对应的凸包。
    OpenCV对轮廓提取凸包的API函数如下：
        void cv::convexHull(
            InputArray points,
            OutputArray hull,
            bool clockwise = false,
            bool returnPoints = true 
        )
    points参数是输入的轮廓点集
    hull凸包检测的输出结果，当参数returnPoints为ture的时候返回凸包的顶点坐标是个点集、returnPoints为false的是返回的是一个integer的vector里面是凸包各个顶点在轮廓点集对应的index
    clockwise 表示顺时针方向或者逆时针方向
    returnPoints表示是否返回点集
    OpenCV中的凸包寻找算法是基于Graham’s扫描法。
    OpenCV中还提供了另外一个API函数用来判断一个轮廓是否为凸包，该方法如下：
        bool cv::isContourConvex(
        InputArray contour
        )
    该方法只有一个输入参数就是轮廓点集。
'''


import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

src = cv.imread("../data/images/hand.jpg")

t = 80
binary = cv.Canny(src, t, t*2) # 边缘检测
# gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
# thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)
k = np.ones((3, 3), dtype=np.uint8)
# 膨胀，最大值滤波，卷积核与图像做卷积，即计算卷积核覆盖的区域的像素点的最大值，并把这个最大值赋值给参考点指定的像素
binary = cv.morphologyEx(binary, cv.MORPH_DILATE, k) 

temp = src.copy()
# 发现轮廓
contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
for c in range(len(contours)):
    cv.drawContours(src, contours, c, (0, 0, 255), 2, cv.LINE_8)
    
    # 跳过面积小于100的轮廓
    area = cv.contourArea(contours[c])
    if area < 100:
        continue

    points = cv.convexHull(contours[c]) # 提取凸包
    is_convex = cv.isContourConvex(contours[c]) # 判断轮廓是否为凸包
    print(f"contours {c}: isContourConvex: {is_convex}")
    is_convex = cv.isContourConvex(points)
    print(f"contours {c} after convexHull: isContourConvex: {is_convex}")
    
    # 将轮廓凸包画出来
    total = len(points)
    for i in range(total):
        x1, y1 = points[i%total][0]
        x2, y2 = points[(i+1)%total][0]
        cv.circle(temp, (x1, y1), 5, (255, 0, 0), 2)
        cv.line(temp, (x1, y1), (x2, y2), (0, 0, 255), 2)
    

# 可视化 
rows = 1
cols = 3
images = [binary, src, temp]
titles = ["binary image", "image"]
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

