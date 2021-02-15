'''
Author       : Bingqiang Zhou
Date         : 2021-02-15 15:35:12
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-15 16:16:10
Description  : 图像梯度 – 拉普拉斯算子(二阶导数算子)
    图像的一阶导数算子可以得到图像梯度局部梯度相应值，二阶导数可以通过快速的图像像素值强度的变化来检测图像边缘，
    其检测图像边缘的原理跟图像的一阶导数有点类似，只是在二阶导数是求X、Y方向的二阶偏导数，对图像来说：

        X方向的二阶偏导数就是 dx = f(x+1, y) + f(x-1, y) – 2*f(x, y)
        Y方向的二阶偏导数就是 dy = f(x, y+1) + f(x, y-1) – 2*f(x, y)

    对X方向与Y方向进行叠加最终就得到delta对应的二阶导数算子，
    下面的部分就是对应的四邻域的二阶导数算子，我们可以进一步扩展增强为八邻域的算子。

    四邻域算子
    0 1 0
    1 -4 1
    0 1 0

    八邻域算子
    1 1 1
    1 -8 1
    1 1 1

    OpenCV中Laplacian滤波函数就是二阶导数发现边缘的函数：
    void cv::Laplacian(
    InputArray src,
    OutputArray dst,
    int ddepth, // 深度默认是-1表示输入与输出图像相同
    int ksize = 1,// 必须是奇数， 等于1是四邻域算子，大于1改用八邻域算子
    double scale = 1,
    double delta = 0, // 对输出图像加上常量值
    int borderType = BORDER_DEFAULT 
    )		

    Python:
    dst	= cv.Laplacian(src, ddepth[, dst[, ksize[, scale[, delta[, borderType]]]] )

    PS:
    拉普拉斯算子是一种特别容易受到噪声干扰的边缘发现算子，所以经常对要处理的图像首先进行一个高斯模糊，然后再进行拉普拉斯算子的边缘提取，而且在一些场景中会把这两步合并成为一步，就是我们经常听说的LOG算子。
    参考：
        https://blog.csdn.net/zaishuiyifangxym/article/details/89840396
        https://blog.csdn.net/swj110119/article/details/51777422
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/lena.jpg")

# 拉普拉斯算子 四邻域
# blured = cv.GaussianBlur(src, ksize=(3, 3), sigmaX=0)
Laplacian_4 = cv.Laplacian(src, cv.CV_32F, ksize=1, scale=1, delta=127)
Laplacian_4 = cv.convertScaleAbs(Laplacian_4)

# 拉普拉斯算子 八邻域
Laplacian_8 = cv.Laplacian(src, cv.CV_32F, ksize=3, scale=1, delta=127)
Laplacian_8 = cv.convertScaleAbs(Laplacian_8)

# 可视化
rows = 1
cols = 3
images = [src, Laplacian_4, Laplacian_8]
titles = ["original image", "Laplacian_4", "Laplacian_8"]
for index, image in enumerate(images):
    plt.subplot(rows, cols, index + 1)
    if index >= len(titles):
        plt.title("image")
    else:
        plt.title(titles[index])
    plt.axis("off")
    plt.imshow(image[:, :, ::-1])
plt.show()
