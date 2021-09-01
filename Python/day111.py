'''
Author       : Bingqiang Zhou
Date         : 2021-09-01 17:00:11
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-01 17:17:13
Description  : KMeans 图像分割
    KMean不光可以对数据进行分类，还可以实现对图像分割，
    什么图像分割，简单的说就要图像的各种像素值，分割为几个指定类别颜色值，
    这种分割有两个应用，一个可以实现图像主色彩的简单提取，
    另外针对特定的应用场景可以实现证件照片的背景替换效果，这个方面早期最好的例子就是证件之星上面的背景替换。
    当然要想实现类似的效果，绝对不是简单的KMeans就可以做到的，还有一系列后续的交互操作需要完成。
    对图像数据来说，要把每个像素点作为单独的样本，按行组织，只需要调用OpenCV的Mat中函数reshape即可实现
    Mat cv::Mat::reshape(
        int cn,
        int rows = 0 
    )const
    cn参数表示通道数
    rows表示改为多少行

    拓展资料：
        官方教程 Understanding K-Means Clustering：https://docs.opencv.org/4.5.3/de/d4d/tutorial_py_kmeans_understanding.html
        官方教程 K-Means Clustering in OpenCV：https://docs.opencv.org/4.5.3/d1/d5c/tutorial_py_kmeans_opencv.html
'''

import cv2 as cv
import numpy as np

img = cv.imread("../data/images/toux.jpg")
data = img.reshape((-1, 3)) # (h*w, 3)
data = np.float32(data) # kmeans输入的数据必须是float32类型
# print(data.shape)

# kmeans 聚类，最多迭代10次，两次差值小于1则停止
retval, labels, centers = cv.kmeans(data, 4, None, (cv.TermCriteria_MAX_ITER + cv.TermCriteria_EPS, 10, 1), 2, cv.KMEANS_RANDOM_CENTERS)
# print(labels.shape, centers.shape)

# 获取labels中元素所对应簇中心的颜色
result = np.uint8(centers[labels.flatten()]) # (h*w, 3)

# reshape到原图像大小
result = result.reshape(img.shape)

# 可视化
cv.imshow("result", result)
cv.waitKey(0)
cv.destroyAllWindows()