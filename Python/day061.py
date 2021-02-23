'''
Author       : Bingqiang Zhou
Date         : 2021-02-23 13:13:14
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-23 14:24:27
Description  : 二值图像分析 – 霍夫圆检测
    根据极坐标,圆上任意一点的坐标可以表示为如下形式, 
        X = x0+rcos(theta)
        Y = y0+rsin(theta)
    所以对于任意一个圆, 假设中心像素点p(x0, y0)像素点已知, 圆半径已知,
    则旋转360由极坐标方程可以得到每个点上得坐标同样,
    如果只是知道图像上像素点，圆半径，旋转360°则中心点处的坐标值必定最强，这正是霍夫变换检测圆的数学原理。

    OpenCV中霍夫圆检测的API与参数解释如下：
    void cv::HoughCircles(
        InputArray image,
        OutputArray circles,
        int method,
        double dp,
        double minDist,
        double param1 = 100,
        double param2 = 100,
        int minRadius = 0,
        int maxRadius = 0 
    )
    image表示输入单通道的灰度图像
    circles 表示检测的圆信息（圆心+半径）
    method 圆检测的方法
    dp表示图像分辨率是否有变化，默认1表示保持跟原图大小一致
    minDist表示检测到的圆，两个圆心之间的最小距离
    param1 表示边缘提取的高阈值
    param2表示霍夫空间的累加阈值
    minRadius 表示可以检测圆的最小半径
    maxRadius 表示可以检测圆的最大

    参考链接：
        霍夫圆变换原理及圆检测 - https://www.cnblogs.com/bjxqmy/p/12333022.html
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/coins.jpg")

gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
# gray = cv.GaussianBlur(gray, (3, 3), 0)
# gray = cv.edgePreservingFilter(gray)

circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 10, param1=100, param2=80, minRadius=20, maxRadius=100)
if circles is not None:
    print(circles.shape)
    for c in circles[0, :]:
        cx, cy, r = c
        cv.circle(src, (cx, cy), int(r), (0, 0, 255), 2)
        cv.circle(src, (cx, cy), 2, (0, 0, 255), cv.FILLED)

# 可视化 
rows = 1
cols = 2
images = [src, gray]
titles = ["original image", "binary image"]
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
