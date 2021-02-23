'''
Author       : Bingqiang Zhou
Date         : 2021-02-23 15:51:23
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-23 16:17:37
Description  : 图像形态学 – 闭操作
    形态学的闭操作跟开操作一样也是基于腐蚀与膨胀两个操作的组合实现的
    闭操作 = 膨胀 + 腐蚀
    闭操作的作用：
    闭操作可以填充二值图像中孔洞区域，形成完整的闭合区域连通组件
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

    其中op指定为MORPH_CLOSE 即表示使用闭操作
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/cells.png")

gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
# gray = cv.GaussianBlur(gray, (9, 9), 0)
thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)

kernel1 = cv.getStructuringElement(cv.MORPH_RECT, (25, 5), (-1, -1)) 
kernel2 = cv.getStructuringElement(cv.MORPH_RECT, (5, 25), (-1, -1))
kernel3 = cv.getStructuringElement(cv.MORPH_CROSS, (15, 15), (-1, -1)) 
result1 = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel1)
result2 = cv.morphologyEx(result1, cv.MORPH_CLOSE, kernel2)
result3 = cv.morphologyEx(result2, cv.MORPH_CLOSE, kernel3, iterations=2)

# 可视化
rows = 2
cols = 2
images = [src, result1, result2, result3]
titles = ["original", "MORPH_CLOSE+RECT+25x5", "MORPH_CLOSE+RECT+5x25", "MORPH_CLOSE+CROSS+15x15"]
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
