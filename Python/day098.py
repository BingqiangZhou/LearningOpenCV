'''
Author       : Bingqiang Zhou
Date         : 2021-08-30 21:11:25
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-30 21:54:04
Description  : SIFT特征提取 – 关键点提取
    SIFT特征提取是图像特征提取中最经典的一个算法，归纳起来SIFT特征提取主要有如下几步：
    -	构建高斯多尺度金字塔
    -	关键点查找/过滤与精准定位
    -	窗口区域角度方向直方图
    -	描述子生成
    SIFT特征是非常稳定的图像特征，在图像搜索、特征匹配、图像分类检测等方面应用十分广泛，
    但是它的缺点也是非常明显，就是计算量比较大，很难实时，所以对一些实时要求比较高的常见SIFT算法还是无法适用。
    如今SIFT算法在深度学习特征提取与分类检测网络大行其道的背景下，已经越来越有鸡肋的感觉，但是它本身的算法知识还是很值得我们学习，
    对我们也有很多有益的启示，本质上SIFT算法是很多常见算法的组合与巧妙衔接，这个思路对我们自己处理问题可以带来很多有益的帮助。
    今天我们首先高清楚SIFT特征提取的前面两个步骤，尺度空间金字塔与关键点过滤。

    OpenCV已经实现了SIFT算法，但是在OpenCV3.0之后因为专利授权问题，该算法在扩展模块xfeature2d中，需要自己编译才可以使用，
    OpenCV Python中从3.4.2之后扩展模块也无法使用，需要自己单独编译python SDK才可以使用。（**在OpenCV Python 4.4中重新加入了SIFT**）
    其使用方法与我们前面介绍的ORB完全一致。都是遵循下面的步骤
    1.	创建对象
    2.	通过detect方法提取对象关键点
    3.	同drawKeypoints绘制关键点

    构建多尺度高斯金字塔
    为了在每组图像中检测 S 个尺度的极值点，DoG 金字塔每组需 S+2 层图像，
    因为每组的第一层和最后一层图像上不能检测极值，DoG 金字塔由高斯金字塔相邻两层相减得到，
    则高斯金字塔每组最少需 S+3 层图像，实际计算时 S 通常在2到5之间。

    拓展资料：
        SIFT特征点提取：https://blog.csdn.net/lingyunxianhe/article/details/79063547
        SIFT特征提取分析：https://blog.csdn.net/abcjennifer/article/details/7639681
        sift、surf、orb 特征提取及最优特征点匹配：https://www.cnblogs.com/multhree/p/11296945.html
        OpenCV官方教程：
            Introduction to SIFT (Scale-Invariant Feature Transform)：https://docs.opencv.org/4.5.3/da/df5/tutorial_py_sift_intro.html
            Feature Matching：https://docs.opencv.org/4.5.3/dc/dc3/tutorial_py_matcher.html
'''

import cv2 as cv
import numpy as np

src = cv.imread("../data/images/test1.png")

# 初始化
sift = cv.SIFT_create()

# 关键点检测
keypoints = sift.detect(src)
# keypoints：[keypoint对象，keypoint对象，...，keypoint对象]
# keypoint类属性：(x, y):坐标, size:关键点邻域直径大小, angle:方向, response:检测的响应值, octave:在那一层金字塔检测到的特征点, class_id:对象类别id

# 可视化
# 全部关键点，使用一个颜色
result = cv.drawKeypoints(src, keypoints, None, (0, 255, 0), cv.DrawMatchesFlags_DEFAULT)

# 关键点，随机一个颜色
result_colorful = src.copy()
for kp in keypoints:
    color = np.random.randint(0, 255, (3), dtype=np.uint8).tolist()
    result_colorful = cv.drawKeypoints(result_colorful, [kp], None, color, cv.DrawMatchesFlags_DEFAULT)

cv.imshow("result", result)
cv.imshow("result colorful", result_colorful)
cv.waitKey(0)
cv.destroyAllWindows()