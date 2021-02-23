'''
Author       : Bingqiang Zhou
Date         : 2021-02-23 22:17:33
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-23 22:39:57
Description  : 图像形态学 – 图像梯度
    图像形态学的梯度跟我们前面介绍的图像卷积计算出来的梯度有本质不同，
    形态学梯度可以帮助我们获得连通组件的边缘与轮廓，实现图像轮廓或者边缘提取。
    根据使用的形态学操作不同，形态学梯度又分为
        -	基本梯度 MORPH_GRADIEN
        -	内梯度 
        -	外梯度
    基本梯度是图像膨胀与腐蚀操作之间的差值
    内梯度是输入图像与腐蚀之间的差值
    外梯度是膨胀与输入图像之间的差值
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
    其中op指定为MORPH_GRADIEN即表示使用基本梯度操作
'''


import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/dennings.jpg")

# gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
# gray = cv.GaussianBlur(gray, (9, 9), 0)
# thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)

kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3), (-1, -1)) 
# 基本梯度，图像膨胀与腐蚀操作之间的差值
result_gradient = cv.morphologyEx(src, cv.MORPH_GRADIENT, kernel) 

# 外梯度，膨胀与输入图像之间的差值
result_dilate = cv.morphologyEx(src, cv.MORPH_DILATE, kernel) # 膨胀操作
result_exteral = cv.subtract(result_dilate, src)

# 内梯度，输入图像与腐蚀之间的差值
result_erode = cv.morphologyEx(src, cv.MORPH_ERODE, kernel) # 腐蚀操作
result_interal = cv.subtract(src, result_erode)

# 内梯度相比外梯度，在各个边缘上面少了一个像素，就是他内缩了一个像素，另外一个是外放了一个像素，整个的边缘外放一个像素

# 可视化
rows = 2
cols = 2
images = [src, result_gradient, result_exteral, result_interal]
titles = ["original", "MORPH_GRADIENT", "result_exteral", "result_interal"]
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


