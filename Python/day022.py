'''
Author       : Bingqiang Zhou
Date         : 2021-02-10 20:43:35
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-10 21:36:20
Description  : 图像均值模糊与高斯模糊
    均值模糊 卷积核的系数完全一致，
    高斯模糊考虑了中心像素距离的影响，对距离中心像素使用高斯分布公式生成不同的权重系数给卷积核，
        然后用此卷积核完成图像卷积得到输出结果就是图像高斯模糊之后的输出。
    OpenCV高斯模糊 API函数
        void GaussianBlur(
            InputArray src, 
            OutputArray dst, 
            Size ksize, // Ksize为高斯滤波器窗口大小
            double sigmaX, // 高斯核在x方向的标准差
            double sigmaY=0, // 高斯核在y方向的标准差
            int borderType=BORDER_DEFAULT // 默认边缘插值方法
            )
    关于参数ksize：
        ksize.width和ksize.height可以不同
        取值有2种情况： 
        可以是正的奇数
        也可以是0，此时它们的值会自动由sigma进行计算
    关于参数sigmaX和sigmaY：
        sigmaY=0时，其值自动由sigmaX确定（sigmaY=sigmaX）；
        sigmaY=sigmaX=0时，它们的值将由ksize.width和ksize.height自动确定；
    
    ksize 越大，他的模糊程度越大，sigma越大，模糊程度也越大。
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/snow.png")

# 均值模糊
dst_5x5 = cv.blur(src, (5, 5))
dst_5x1 = cv.blur(src, (5, 1)) # 只对一个方向x方向做模糊

# 高斯模糊
dst_g_5x5 = cv.GaussianBlur(src, (5, 5), 15)
dst_g_5x1 = cv.GaussianBlur(src, (5, 1), 15) # 只对一个方向x方向做模糊
dst_g_0x0 = cv.GaussianBlur(src, (0, 0), 15) # size设置为0

# 可视化
rows = 2
cols = 3
plt.subplot(rows, cols, 1)
plt.title("src")
plt.axis("off")
plt.imshow(src[:, :, ::-1])
plt.subplot(rows, cols, 2)
plt.title("blur 5x5")
plt.axis("off")
plt.imshow(dst_5x5[:, :, ::-1])
plt.subplot(rows, cols, 3)
plt.title("blur 5x1")
plt.axis("off")
plt.imshow(dst_5x1[:, :, ::-1])

plt.subplot(rows, cols, 4)
plt.title("GaussianBlur 5x5")
plt.axis("off")
plt.imshow(dst_g_5x5[:, :, ::-1])
plt.subplot(rows, cols, 5)
plt.title("GaussianBlur 5x1")
plt.axis("off")
plt.imshow(dst_g_5x5[:, :, ::-1])
plt.subplot(rows, cols, 6)
plt.title("GaussianBlur 0x0")
plt.axis("off")
plt.imshow(dst_g_0x0[:, :, ::-1])
plt.show()