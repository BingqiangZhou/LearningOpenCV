'''
Author       : Bingqiang Zhou
Date         : 2021-02-23 23:22:52
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-23 23:36:53
Description  : 形态学操作 – 击中击不中
    形态学的击中击不中操作，根据结构元素不同，可以提取二值图像中的一些特殊区域，得到我们想要的结果。
    击中击不中操作的API也是我们前面一直用的API，只是对OP参数的修改
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
    其中op指定为MORPH_HITMISS即表示使用击中击不中
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/cross.png")

gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY_INV)

kernel = cv.getStructuringElement(cv.MORPH_CROSS, (15, 15), (-1, -1)) 
result_hitmiss = cv.morphologyEx(binary, cv.MORPH_HITMISS, kernel)

# 就是说我有一个结构元素，如果你跟结构元素完全一致，你就保留，如果你跟结构元素不一致，你就得消失。

# 可视化
rows = 1
cols = 3
images = [src, binary, result_hitmiss]
titles = ["original", "THRESH_BINARY_INV", "MORPH_HITMISS"]
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
