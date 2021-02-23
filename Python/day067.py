'''
Author       : Bingqiang Zhou
Date         : 2021-02-23 21:22:32
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-23 21:55:58
Description  : 图像形态学 – 顶帽操作
    形态学的顶帽操作是图像输入与开操作之间的差异，顶帽操作有时候对于我们提取图像中微小部分特别有用，顶帽操作：
    顶帽 = 原图 – 开操作
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
    其中op指定为MORPH_TOPHAT 即表示使用顶帽操作
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/cells.png")

gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
# gray = cv.GaussianBlur(gray, (9, 9), 0)
thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)

kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5), (-1, -1)) 
result_open = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel) # 开操作，
result_tophat = cv.morphologyEx(binary, cv.MORPH_TOPHAT, kernel) # 顶帽操作，得到开操作丢失的部分

# 可视化
rows = 1
cols = 3
images = [src, result_open, result_tophat]
titles = ["original", "MORPH_OPEN", "MORPH_TOPHAT"]
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
