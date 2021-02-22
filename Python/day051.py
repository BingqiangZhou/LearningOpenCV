'''
Author       : Bingqiang Zhou
Date         : 2021-02-22 14:39:57
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-22 15:37:27
Description  : 二值图像分析 – 使用轮廓逼近
    对图像二值图像的每个轮廓，可以使用轮廓逼近，
    逼近每个轮廓的真实几何形状，从而通过轮廓逼近的输出结果判断一个对象是什么形状。
    OpenCV轮廓逼近的API如下：
        void cv::approxPolyDP(
            InputArray curve,
            OutputArray approxCurve,
            double epsilon,
            bool closed 
        )
    其中
    Curve表示轮廓曲线
    approxCurve 表示轮廓逼近输出的顶点数目
    epsilon 轮廓逼近的顶点距离真实轮廓曲线的最大距离，该值越小表示越逼近真实轮廓
    close 表示是否为闭合区域
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/contours.png")

gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)

# 发现轮廓
contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# print(hierarchy, hierarchy.shape)
for c in range(len(contours)):
    cv.drawContours(src, contours, c, (0, 0, 255), 2, cv.LINE_8)
    result = cv.approxPolyDP(contours[c], 4, True)
    vertexes = result.shape[0] # 点的个数
    rect = cv.minAreaRect(contours[c]) # 获取轮廓最小外接矩形
    cx, cy = rect[0] # 获取中心坐标
    if vertexes == 3:
        cv.putText(src, "triangle", (int(cx), int(cy)), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    elif vertexes == 4:
        cv.putText(src, "rectangle", (int(cx), int(cy)), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    elif vertexes < 10:
        cv.putText(src, "ploy", (int(cx), int(cy)), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    elif vertexes >= 10:
        cv.putText(src, "circle", (int(cx), int(cy)), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)


# 可视化 
rows = 1
cols = 2
images = [binary, src]
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

