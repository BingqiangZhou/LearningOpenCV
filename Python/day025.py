'''
Author       : Bingqiang Zhou
Date         : 2021-02-11 14:33:36
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-11 15:33:29
Description  : 图像去噪声
    图像去噪声在OCR、机器人视觉与机器视觉领域应用开发中是重要的图像预处理手段之一，对图像二值化与二值分析很有帮助.
    OpenCV中常见的图像去噪声的方法有
    - 均值去噪声
    - 高斯模糊去噪声
    - 非局部均值去噪声
    - 双边滤波去噪声 (后面再介绍)
    - 形态学去噪声 (后面再介绍)
    一般卷积核大小从3x3尝试起，卷积核大小不易过大，过大会丢失大量图像原有细节。
'''

import cv2 as cv
import numpy as np

# 图像椒盐噪声生成
def generate_salt_pepper_noise(image):
    dst = np.copy(image)
    h, w = dst.shape[:2]
    nums = 1000 # 产生椒盐噪声的点数
    x = np.random.randint(0, w, nums) # 随机x坐标
    y = np.random.randint(0, h, nums) # 随机y坐标
    for index, pos in enumerate(zip(y, x)):
        # 产生白噪声或者黑噪声
        if index % 2 == 0:
            dst[pos] = 255
        else:
            dst[pos] = 0
    return dst

# 图像高斯噪声生成
def generate_gaussian_noise(image):
    noise = np.zeros_like(image)
    mean = (15, 15, 15)
    stddev = (30, 30, 30)
    cv.randn(noise, mean, stddev) # 随机产生高斯噪声
    dst = cv.add(image, noise)
    return dst

src = cv.imread("../data/images/lena.jpg")
dst_salt_pepper = generate_salt_pepper_noise(src) # 图像椒盐噪声生成
dst_gaussian = generate_gaussian_noise(src) # 图像高斯噪声生成

## 均值模糊
dst_salt_pepper_blur = cv.blur(dst_salt_pepper, ksize=(5, 5))
dst_gaussian_blur = cv.blur(dst_gaussian, ksize=(5, 5))

## 中值模糊，ksize为大于1的奇数
dst_salt_pepper_median = cv.medianBlur(dst_salt_pepper, 5)
dst_gaussian_blur_median = cv.medianBlur(dst_gaussian_blur, 5)

## 高斯模糊
dst_salt_pepper_gaussian = cv.GaussianBlur(dst_salt_pepper, (5, 5), 15)
dst_gaussian_blur_gaussian = cv.GaussianBlur(dst_gaussian_blur, (5, 5) , 15)

## 非局部均值去噪，搜索框一般是模版框大小的3倍
dst_salt_pepper_nlmean = cv.fastNlMeansDenoisingColored(dst_salt_pepper, h=15, hColor=15, templateWindowSize=10, searchWindowSize=30)
dst_gaussian_blur_nlmean = cv.fastNlMeansDenoisingColored(dst_gaussian_blur, h=15, hColor=15, templateWindowSize=10, searchWindowSize=30)

# 可视化
# cv.imshow("original image", src)
cv.imshow("dst_salt_pepper", dst_salt_pepper)
cv.imshow("dst_gaussian", dst_gaussian)
cv.imshow("dst_salt_pepper_blur", dst_salt_pepper_blur)
cv.imshow("dst_gaussian_blur", dst_gaussian_blur)
cv.imshow("dst_salt_pepper_median", dst_salt_pepper_median)
cv.imshow("dst_gaussian_blur_median", dst_gaussian_blur_median)
cv.imshow("dst_salt_pepper_gaussian", dst_salt_pepper_gaussian)
cv.imshow("dst_gaussian_blur_gaussian", dst_gaussian_blur_gaussian)
cv.imshow("dst_salt_pepper_nlmean", dst_salt_pepper_nlmean)
cv.imshow("dst_gaussian_blur_nlmean", dst_gaussian_blur_nlmean)

cv.waitKey(0)
cv.destroyAllWindows()
