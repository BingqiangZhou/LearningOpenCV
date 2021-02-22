'''
Author       : Bingqiang Zhou
Date         : 2021-02-23 01:11:49
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-23 01:47:32
Description  : 二值图像分析 – 寻找最大内接圆
    对于轮廓来说，有时候我们会需要选择最大内接圆，OpenCV中没有现成的API可以使用，
    但是我们可以通过点多边形测试巧妙的获取轮廓最大内接圆的半径，
    从点多边形测试的返回结果我们知道，它返回的是像素距离，而且是当前点距离轮廓最近的距离，
    当这个点在轮廓内部，其返回的距离是最大值的时候，其实这个距离就是轮廓的最大内接圆的半径，
    这样我们就巧妙的获得了圆心的位置与半径，剩下的工作就很容易了完成，绘制一个圆而已，一行代码就可以搞定，
    而且前面我们的知识点分享已经交代了如何在OpenCV中去绘制常见几何形状啦。
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# 画出一个多边形
r = 100
binary = np.zeros((4*r, 4*r), dtype=np.uint8)
vert = [None]*6
vert[0] = (3*r//2, int(1.34*r))
vert[1] = (1*r, 2*r)
vert[2] = (3*r//2, int(2.866*r))
vert[3] = (5*r//2, int(2.866*r))
vert[4] = (3*r, 2*r)
vert[5] = (5*r//2, int(1.34*r))
for i in range(6):
    cv.line(binary, vert[i],  vert[(i+1)%6], (255), 3)

# 发现轮廓
contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

dist = np.zeros_like(binary, dtype=np.float32)
result = np.zeros((4*r, 4*r, 3), dtype=np.float32)
h, w = dist.shape[:2]
for row in range(h):
    for col in range(w):
        dist[row, col] = cv.pointPolygonTest(contours[0], (col, row), True)

        if dist[row, col] > 0: # 在多边形内
            result[row, col] = (255-dist[row, col], 0, 0)
        elif dist[row, col] < 0: # 在多边形外
            result[row, col] = (0, 0, 255-dist[row, col])
        else: # dist == 0，在多边形边缘上
            result[row, col] = (0, 255, 0)

result = cv.convertScaleAbs(result)

min_val, max_val, min_loc, max_loc = cv.minMaxLoc(dist)
# print(min_val, max_val, min_loc, max_loc)

# 绘制最大外接圆
cv.circle(result, max_loc, int(max_val), (0, 255, 0), 2)

# 可视化 
rows = 1
cols = 2
images = [binary, result]
titles = ["binary image", "result"]
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
