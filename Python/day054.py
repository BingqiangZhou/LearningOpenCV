'''
Author       : Bingqiang Zhou
Date         : 2021-02-22 16:55:31
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-22 17:28:51
Description  : 二值图像分析 – 对轮廓圆与椭圆拟合
    有时候我们需要对找到的轮廓点进行拟合，生成一个拟合的圆形或者椭圆，
    以便我们对轮廓进行更进一步的处理，满足我们对最终轮廓形状的判断，
    OpenCV对轮廓进行圆形或者椭圆拟合的API函数如下：
        RotatedRect cv::fitEllipse(
        InputArray points
        )
    参数points是轮廓点，
    输出RotatedRect包含下面三个信息
    -	拟合之后圆或者椭圆的中心位置、
    -	长轴与短轴的直径
    -	角度
    然后我们就可以根据得到拟合信息绘制椭圆、当长轴与短轴相等的时候就是圆。
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

src = cv.imread("../data/images/stuff.jpg")

t = 80
binary = cv.Canny(src, t, t*2) # 边缘检测
k = np.ones((3, 3), dtype=np.uint8)
# 膨胀，最大值滤波，卷积核与图像做卷积，即计算卷积核覆盖的区域的像素点的最大值，并把这个最大值赋值给参考点指定的像素
binary = cv.morphologyEx(binary, cv.MORPH_DILATE, k) 

# 发现轮廓
contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
for c in range(len(contours)):
    # 椭圆拟合
    (cx, cy), (a, b), angle = cv.fitEllipse(contours[c])
    # 绘制椭圆
    cv.ellipse(src, (int(cx), int(cy)), (int(a/2), int(b/2)), angle, 0, 360, (0, 0, 255), 2)
    
    # 标注圆形
    ratio = min(a, b) / max(a, b)
    if ratio <= 1 and ratio > 0.9:
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


