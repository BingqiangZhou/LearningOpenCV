'''
Author       : Bingqiang Zhou
Date         : 2021-02-23 16:44:35
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-23 17:06:53
Description  : 图像形态学 – 开闭操作时候结构元素应用演示
    OpenCV中图像形态学开操作与闭操作，根据结构元素的不同可以实现不同的二值图像处理效果，
    我们可以通过下面的结构元素对图像进行开操作，提取二值图像中水平与垂直线，
    这个方法比霍夫直线检测要好用得多， 在一些应用场景中会特别有用，图像分析、OCR布局分析中形态学操作十分重要，
    我们通过两个例子来说明开闭操作的作用。
    一，开操作提取水平线，实现填空题横线位置提取
        结构元素大小为20x1
        其步骤分为：
        1.	转灰度
        2.	转二值，可选降噪
        3.	形态学操作，提取水平线
        4.	轮廓发现，确定位置

    二，闭操作实现不同层次的轮廓填充
        结构元素分为两种：
        矩形结构元素25x25大小
        圆形结构元素15x15大小
'''

import cv2 as cv
import matplotlib.pyplot as plt

# 一，开操作提取水平线，实现填空题横线位置提取
src1 = cv.imread("../data/images/fill.png")

# 1.转灰度
gray = cv.cvtColor(src1, cv.COLOR_BGR2GRAY)
# 2.转二值，可选降噪
thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY_INV)
# 3.形态学操作，提取水平线
kernel1 = cv.getStructuringElement(cv.MORPH_RECT, (20, 1), (-1, -1)) 
result1 = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel1)
# 4.轮廓发现，确定位置
contours, hierarchy = cv.findContours(result1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
for c in range(len(contours)):
    x, y, w, h = cv.boundingRect(contours[c])
    cv.rectangle(src1, (x, y), (x+w, y-15), (0, 0, 255), 2)


# 二，闭操作实现不同层次的轮廓填充
src2 = cv.imread("../data/images/morph3.png")
kernel2 = cv.getStructuringElement(cv.MORPH_RECT, (25, 25))
result2 = cv.morphologyEx(src2, cv.MORPH_CLOSE, kernel2)
kernel3 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (25, 25))
result3 = cv.morphologyEx(src2, cv.MORPH_CLOSE, kernel3)


# 可视化
rows = 2
cols = 3
images = [src1, binary, result1, src2, result2, result3]
titles = ["result 1", "binary 1", "morph result 1", "src 2", "MORPH_RECT 25x25", "MORPH_ELLIPSE 25x25"]
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

