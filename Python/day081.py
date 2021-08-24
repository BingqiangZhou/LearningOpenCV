'''
Author       : Bingqiang Zhou
Date         : 2021-08-24 23:16:19
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-24 23:51:57
Description  : 角点检测 – Harris角点检测
    角点是一幅图像上最明显与重要的特征，对于一阶导数而言，角点在各个方向的变化是最大的，而边缘区域在只是某一方向有明显变化

    OpenCV中相关API与解释如下：
    void cv::cornerHarris(
        InputArray src,
        OutputArray dst,
        int blockSize,
        int ksize,
        double k,
        int borderType = BORDER_DEFAULT
    )
    src单通道输入图像
    dst是输出response
    blockSize计算协方差矩阵的时候邻域像素大小
    ksize表示soble算子的大小
    k表示系数，一般设置为0.04～0.06（经验）
'''
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def detecting_corners(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    dst = cv.cornerHarris(gray, blockSize=2, ksize=3, k=0.04)
    dst_norm = np.zeros_like(dst, dtype=np.float32)
    cv.normalize(dst, dst_norm, 0, 255, cv.NORM_MINMAX)
    # draw circle for corner
    index = np.argwhere(dst_norm > 155)
    for y, x in index:
        color = np.random.randint(0, 256, (3), dtype=np.int32)
        image = cv.circle(image, (x, y), 5, (int(color[0]), int(color[1]), int(color[2])), 2)
    
    return image

src = cv.imread("../data/images/lena.jpg")
detecting_corners(src)

# 可视化
rows = 1
cols = 1
images = [src]
titles = ["original image"]
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