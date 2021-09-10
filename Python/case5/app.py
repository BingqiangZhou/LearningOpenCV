'''
Author       : Bingqiang Zhou
Date         : 2021-09-10 22:04:49
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-11 00:55:30
Description  : 案例五 - 分水岭分割案例
    基于分水岭对象分割实现计数的例子，算法的主要步骤可以拆解为如下：
        第一步：加载图像
        第二步：去噪声，这步要根据实际图像来看，去噪声的方法很多，高斯模糊、双边、均值迁移、非局部均值去噪声等方法
        第三步：灰度化与二值化，选择合适二值化方法也很重要
        第四步：距离变换 + 阈值处理
        第五步：寻找与标记marker
        第六步：根据marker实现图像分水岭分割
        第七步：根据marker生成颜色填充
    
    官方教程：Image Segmentation with Watershed Algorithm - https://docs.opencv.org/master/d3/db4/tutorial_py_watershed.html
'''

import cv2 as cv
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt

# 加载图像
image = cv.imread("./images/pills.png")
# image = cv.imread("./images/coins.png")
cv.imshow("step 1", image)

# 去噪声
image = cv.pyrMeanShiftFiltering(image, 21, 51)
cv.imshow("step 2", image)


# 灰度化与二值化
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY)
cv.imshow("step 3", binary)

# 距离变换 + 阈值处理
dist = cv.distanceTransform(binary, cv.DIST_L2, 3) # 不等于0的值到0值的最小距离
ret, binary = cv.threshold(dist, 0.5*dist.max(), 255, cv.THRESH_BINARY)
cv.imshow("step 4", binary)

# 寻找与标记marker (将不同的独立的形状标记成不同的数字)，0表示未知标记，1、2、……、n表示背景与前景
# 方式一：找到轮廓，填充轮廓
# 方式二：使用形态学操作确认前背景像素以及不确定的像素，再用连通组件做标记，这种方法更加通用，见官方教程
markers = binary.astype(np.uint8)
contours, hierarchy = cv.findContours(markers, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
object_marker = 1
for i in range(len(contours)):
    cv.drawContours(markers, contours, i, (object_marker), -1)
    object_marker += 1

cv.circle(markers, (5, 5), 5, (object_marker), -1) # 背景，在左上角画一个5x5大小的圆作为确定的背景像素
cv.imshow("step 5", markers)

# 根据marker实现图像分水岭分割
markers = cv.watershed(image, markers.astype(np.int32))
markers[markers == -1] = 0 # -1 为对象边缘
cv.imshow("markers == -1", (markers == 0).astype(np.uint8)*255)
cv.imshow("step 6", markers.astype(np.uint8))

# 根据marker生成颜色填充
# https://matplotlib.org/stable/tutorials/colors/colormaps.html
# https://github.com/BingqiangZhou/Interactive-Multi-target-Segmentation/blob/master/demo/codes/utils.py
color_map_name = "tab20"
color_map = plt.get_cmap(color_map_name)
rgb_array = cm.get_cmap(color_map)(np.linspace(0, 1, num=color_map.N), bytes=True)[:, :3] # RGBA
seg_image = rgb_array[markers]
cv.imshow("step 7", seg_image)

cv.waitKey(0)
cv.destroyAllWindows()
