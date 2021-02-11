'''
Author       : Bingqiang Zhou
Date         : 2021-02-09 11:03:30
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-11 14:23:32
Description  : 图像直方图均衡化
    图像直方图均衡化可以用于图像增强、对输入图像进行直方图均衡化处理，提升后续对象检测的准确率在OpenCV人脸检测的代码演示中已经很常见。
    此外对医学影像图像与卫星遥感图像也经常通过直方图均衡化来提升图像质量。

    OpenCV中直方图均衡化的API很简单
    - equalizeHist(src, dst)
    
    直方图均衡化原理可参考：
        https://zhuanlan.zhihu.com/p/44918476
        https://blog.csdn.net/qq_15971883/article/details/88699218 (有手算过程)
    
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def custom_equalizeHist(image, show_figure=True):
    h, w = image.shape[:2]
    if image.ndim > 1:
        print("cvt to gray")
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    hist = np.zeros((256), np.uint)
    equalized_hist = np.zeros((256), np.uint)
    
    # 计算各个通道的直方图
    for row in range(h):
        for col in range(w):
            hist[image[row, col]] += 1

    # 直方图均衡化
    hists_cumsum = np.cumsum(hist)
    mapping_func = np.round(hists_cumsum / (h * w) * (256-1)).astype("uint8")
    for i in range(256):
        equalized_hist[mapping_func[i]] += hist[i]
    
    # 映射，赋值，生成均衡化后的图像
    equalized_image = mapping_func[image]

    if show_figure:
        # 可视化相关图像：原图像灰度图、custom计算的均衡化后的图像
        plt.figure("images")
        plt.subplot(2, 3, 1)
        plt.imshow(image, cmap='gray')

        plt.subplot(2, 3, 2)
        plt.imshow(equalized_image, cmap='gray')

        plt.subplot(2, 3, 3)
        dst = cv.equalizeHist(image)
        dst_hist = cv.calcHist([dst], [0], None, [256], [0, 256])
        print("equalized_image: ", not np.any(dst - equalized_image)) ## 判断是否与opencv中的equalizeHist输出一致
        print("equalized_hist: ", not np.any(dst_hist[:, 0] - equalized_hist)) ## 判断是否与opencv中的均衡化后的直方图输出一致
        plt.imshow(dst, cmap='gray')
        
        plt.subplot(2, 3, 4)
        plt.plot(hist)
        
        plt.subplot(2, 3, 5)
        plt.plot(equalized_hist)
        
        plt.subplot(2, 3, 6)
        plt.plot(dst_hist)
        
        plt.show()

    return equalized_image, hist, equalized_hist

src = cv.imread("../data/images/cos.jpg")
rgb = cv.cvtColor(src, cv.COLOR_BGR2RGB)

## 调用opencv api进行均衡化
equalized_images = []
bgr = cv.split(src)
plt.figure(figsize=(4, 8))
for index, gray in enumerate(bgr):
    hist = cv.calcHist([gray], [0], None, [256], [0, 256])          # 计算均衡化前的直方图
    dst = cv.equalizeHist(gray)                                     # 直方图均衡化
    equalized_hist = cv.calcHist([dst], [0], None, [256], [0, 256]) # 计算均衡化后的直方图
    equalized_images.append(dst)
    plt.subplot(4, 2, index*2+1)
    plt.title("bgr"[index])
    plt.plot(hist)                                                  # 可视化均衡化前的直方图
    
    plt.subplot(4, 2, index*2+2)
    plt.title("bgr"[index]+" equalized")
    plt.plot(equalized_hist)                                        # 可视化均衡化后的直方图

plt.subplot(4, 2, 7)
plt.imshow(rgb)

plt.subplot(4, 2, 8)
plt.imshow(cv.merge(equalized_images))                              # 可视化合并的衡化后图

plt.show()

## 调用自行实现的直画图均衡化
custom_equalizeHist(src)
