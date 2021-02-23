'''
Author       : Bingqiang Zhou
Date         : 2021-02-23 15:24:58
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-23 15:47:16
Description  : 图像形态学 – 开操作
    形态学的开操作是基于腐蚀与膨胀两个操作的组合实现的
    开操作 = 腐蚀 + 膨胀
    开操作的作用：
    开操作可以删除二值图像中小的干扰块，降低图像二值化之后噪点过多的问题，

    void cv::morphologyEx(
        InputArray src,
        OutputArray dst,
        int op,
        InputArray kernel,
        Point anchor = Point(-1,-1),
        int iterations = 1,
        int borderType = BORDER_CONSTANT,
    )

    src 输入图像
    dst 输出图像
    op 形态学操作
    kernel 结构元素
    anchor 中心位置锚定
    iterations 循环次数
    borderType 边缘填充类型

    其中op指定为MORPH_OPEN 即表示使用开操作
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/shuini.jpg")

gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
gray = cv.GaussianBlur(gray, (9, 9), 0)
# thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)
binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 45, 15)

ksize = (5, 5)
kernel = cv.getStructuringElement(cv.MORPH_RECT, ksize, (-1, -1)) 
result = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)

# 可视化
rows = 1
cols = 3
images = [src, binary, result]
titles = ["original", "binary", "MORPH_OPEN"]
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


