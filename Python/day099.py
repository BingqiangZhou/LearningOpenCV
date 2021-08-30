'''
Author       : Bingqiang Zhou
Date         : 2021-08-30 21:48:47
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-30 21:59:27
Description  : SIFT特征提取 – 描述子生成
    SIFT特征提取是图像特征提取中最经典的一个算法，归纳起来SIFT特征提取主要有如下几步：
    -	构建高斯多尺度金字塔
    -	关键点查找/过滤与精准定位
    -	窗口区域角度方向直方图
    -	描述子生成
    前面我们已经详细解释了SIFT特征点是如何提取的，有了特征点之后，我们对特征点周围的像素块计算角度方向直方图，
    在计算直方图之前首先需要对图像进行梯度计算，这里可以使用SOBEL算子，然后根据dx与dy计算梯度和与角度。
    
    拓展资料：
    SIFT特征点提取：https://blog.csdn.net/lingyunxianhe/article/details/79063547
    SIFT特征提取分析：https://blog.csdn.net/abcjennifer/article/details/7639681
    sift、surf、orb 特征提取及最优特征点匹配：https://www.cnblogs.com/multhree/p/11296945.html
    OpenCV官方教程：
        Introduction to SIFT (Scale-Invariant Feature Transform)：https://docs.opencv.org/4.5.3/da/df5/tutorial_py_sift_intro.html
        Feature Matching：https://docs.opencv.org/4.5.3/dc/dc3/tutorial_py_matcher.html
'''

import cv2 as cv

box_in_scene = cv.imread("../data/images/box_in_scene.png")
box = cv.imread("../data/images/box.png")

# 初始化
sift = cv.SIFT_create()

# 关键点检测以及计算特征描述子
keypoints_box_in_scene, descriptors_box_in_scene = sift.detectAndCompute(box_in_scene, None)
keypoints_box, descriptors_box = sift.detectAndCompute(box, None)
# keypoints：[keypoint对象，keypoint对象，...，keypoint对象]
# keypoint类属性：(x, y):坐标, size:关键点邻域直径大小, angle:方向, response:检测的响应值, octave:在那一层金字塔检测到的特征点, class_id:对象类别id
# descriptors: (nfeatures, 128)

# 使用汉明距离，暴力一对一匹配
# bf = cv.BFMatcher_create(cv.NORM_HAMMING, crossCheck=True)
bf = cv.DescriptorMatcher_create(cv.DescriptorMatcher_BRUTEFORCE)
matches = bf.match(descriptors_box, descriptors_box_in_scene) # 注意这里, 前面是query，后面是train
good_matches = sorted(matches, key=lambda x: x.distance)[:10] # 取距离最小的10个，即匹配度最高的10个

# 可视化
# 注意这里, 需要与生成match的顺序对应，前面是query，后面是train
result = cv.drawMatches(box, keypoints_box, box_in_scene, keypoints_box_in_scene, good_matches, None)
cv.imshow("result", result)
cv.waitKey(0)
cv.destroyAllWindows()
