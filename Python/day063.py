'''
Author       : Bingqiang Zhou
Date         : 2021-02-23 15:08:44
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-23 15:34:59
Description  : 图像形态学 - 膨胀与腐蚀
    膨胀与腐蚀操作不仅可以对二值图像有效操作，对彩色与灰度图像也有作用，
    对于二值图像的腐蚀与膨胀来说，选择一个好的结构元素至关重要，
    OpenCV中获取结构元素的API与参数解释如下：
        Mat cv::getStructuringElement(
            int shape,
            Size ksize,
            Point anchor = Point(-1,-1)
        )
    shape是指结构元素的类型，常见的有矩形(MORPH_RECT)、圆形(MORPH_ELLIPSE)、十字交叉(MORPH_CROSS)
    ksize 是指结构元素大小
    anchor 中心锚点的位置
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/coins.jpg")

gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)

ksize = (5, 5)
kernel_rect = cv.getStructuringElement(cv.MORPH_RECT, ksize, (-1, -1))
kernel_ellipse = cv.getStructuringElement(cv.MORPH_ELLIPSE, ksize, (-1, -1))
kernel_cross = cv.getStructuringElement(cv.MORPH_CROSS, ksize, (-1, -1))
print(kernel_rect, kernel_ellipse, kernel_cross, sep="\n")
dilate_dst = cv.dilate(binary, kernel_rect)
erode_dst = cv.erode(binary, kernel_ellipse)
result = cv.dilate(erode_dst, kernel_cross, iterations=3) # 迭代三次

# 可视化
rows = 2
cols = 2
images = [binary, dilate_dst, erode_dst, result]
titles = ["binary", "dilate", "erode", "erode+dilate"]
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

