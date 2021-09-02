'''
Author       : Bingqiang Zhou
Date         : 2021-09-02 14:00:42
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-02 14:32:36
Description  : Grabcut图像分割
    Grabcut是基于图割(graph cut)实现的图像分割算法，
    它需要用户输入一个bounding box作为分割目标位置，实现对目标与背景的分离/分割，
    这个跟KMeans与MeanShift等图像分割方法有很大的不同，但是Grabcut分割速度快，效果好，支持交互操作，
    因此在很多APP图像分割/背景虚化的软件中可以看到其身影。
    void cv::grabCut(
        InputArray 	img,
        InputOutputArray 	mask,
        Rect 	rect,
        InputOutputArray 	bgdModel,
        InputOutputArray 	fgdModel,
        int 	iterCount,
        int 	mode = GC_EVAL 
    )
    img输入的三通道图像
    mask输入的单通道图像，初始化方式为GC_INIT_WITH_RECT表示ROI区域可以被初始化为：
    GC_BGD 定义为明显的背景像素 0
    GC_FGD 定义为明显的前景像素 1
    GC_PR_BGD 定义为可能的背景像素 2
    GC_PR_FGD 定义为可能的前景像素 3
    rect 表示roi区域
    bgdModel表示临时背景模型数组
    fgdModel表示临时前景模型数组
    iterCount表示图割算法迭代次数
    mode当使用用户提供的roi时候使用GC_INIT_WITH_RECT

    拓展资料：
        官方教程：Interactive Foreground Extraction using GrabCut Algorithm：https://docs.opencv.org/4.5.3/d8/d83/tutorial_py_grabcut.html
'''

import cv2 as cv
import numpy as np

img = cv.imread("../data/images/master.jpg")
rect = cv.selectROI("select roi", img, showCrosshair=True) # 交互选取分割目标区域

# 初始化mask 以及 前背景模型，注意这里的类型
bgdModel = np.zeros((1, 65), dtype=np.float64) # float64
fgdModel = np.zeros((1, 65), dtype=np.float64)
mask = np.zeros(img.shape[:2], dtype=np.uint8)

# grabcut分割
mask, bgdModel, fgdModel = cv.grabCut(img, mask, rect, bgdModel, fgdModel, 6, cv.GC_INIT_WITH_RECT)
fg_mask = np.where((mask == 1) + (mask == 3), 255, 0).astype(np.uint8)

# 提取分割得到的前景对象
result = cv.bitwise_and(img, img, mask=fg_mask)
cv.imshow("result", result)
cv.waitKey(0)
cv.destroyAllWindows()