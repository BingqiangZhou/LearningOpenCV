'''
Author       : Bingqiang Zhou
Date         : 2021-02-15 13:17:44
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-15 13:40:30
Description  : 图像梯度 – Sobel算子
    卷积的作用除了实现图像模糊或者去噪，还可以寻找一张图像上所有梯度信息，这些梯度信息是图像的最原始特征数据，
    进一步处理之后就可以生成一些比较高级的特征用来表示一张图像实现基于图像特征的匹配，图像分类等应用。
    Sobel算子是一种很经典的图像梯度提取算子，其本质是基于图像空间域卷积，背后的思想是图像一阶导数算子的理论支持。
    
    Sobel算子X方向  Y方向 
    -1 0 +1     -1 -2 -1
    -2 0 +2     0  0  0
    -1 0 +1     +1 +2 +1

    Scharr算子X方向  Y方向 
    -3 0 +3     -3 -10 -3
    -10 0 +10     0  0  0
    -3 0 +3     +3 +10 +3
    
    OpenCV实现了基于Sobel算子提取图像梯度的API，表示与解释如下：
        void cv::Sobel(
        InputArray src, // 输入图像
        OutputArray dst, // 输出结果
        int ddepth, // 图像深度CV_32F
        int dx,// 1，X方向 一阶导数
        int dy, // 1，Y方向 一阶导数
        int ksize = 3, // 窗口大小
        double scale = 1, // 放缩比率，1 表示不变
        double delta = 0, // 对输出结果图像加上常量值
        int borderType = BORDER_DEFAULT 
        )		
    Python:
        dst = cv.Sobel(src, ddepth, dx, dy[, dst[, ksize[, scale[, delta[, borderType]]]]])
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/lena.jpg")

# Sobel算子
sobel_x_grad = cv.Sobel(src, cv.CV_32F, 1, 0, ksize=3) # x方向
sobel_y_grad = cv.Sobel(src, cv.CV_32F, 0, 1, ksize=3) # y方向

sobel_x_grad = cv.convertScaleAbs(sobel_x_grad)
sobel_y_grad = cv.convertScaleAbs(sobel_y_grad)

sobel_xy_grad = cv.add(sobel_x_grad, sobel_y_grad, dtype=cv.CV_16S)
sobel_xy_grad = cv.convertScaleAbs(sobel_xy_grad)

# Scharr算子
scharr_x_grad = cv.Scharr(src, cv.CV_32F, 1, 0) # x方向
scharr_y_grad =cv.Scharr(src, cv.CV_32F, 0, 1) # y方向

scharr_x_grad = cv.convertScaleAbs(scharr_x_grad)
scharr_y_grad = cv.convertScaleAbs(scharr_y_grad)

scharr_xy_grad = cv.add(scharr_x_grad, scharr_y_grad, dtype=cv.CV_16S)
scharr_xy_grad = cv.convertScaleAbs(scharr_xy_grad)

# 可视化
rows = 2
cols = 4
images = [src, sobel_x_grad, sobel_y_grad, sobel_xy_grad, 
            scharr_x_grad, scharr_y_grad, scharr_xy_grad]
titles = ["original image", "sobel_x_grad", "sobel_y_grad", "sobel_x+y_grad", 
            "scharr_x_grad", "scharr_y_grad", "scharr_x+y_grad"]
for index, image in enumerate(images):
    plt.subplot(rows, cols, index + 1)
    if index >= len(titles):
        plt.title("image")
    else:
        plt.title(titles[index])
    plt.axis("off")
    plt.imshow(image[:, :, ::-1])
plt.show()
