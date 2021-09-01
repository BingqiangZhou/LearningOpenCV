'''
Author       : Bingqiang Zhou
Date         : 2021-09-01 10:34:30
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-01 10:49:26
Description  : Brisk特征提取与描述子匹配
    BRISK(Binary robust invariant scalable keypoints)是一种基于尺度空间不变性类似ORB特征描述子的特征提取算法。
    BRISK主要步骤可以分为如下两步：
    1.	构建尺度空间金字塔实现关键点定位
    2.	根据关键点生成描述子
    拓展资料：
        【特征检测】BRISK特征提取算法：https://www.cnblogs.com/decode1234/p/12124415.html

'''

import cv2 as cv

box_in_scene = cv.imread("../data/images/box_in_scene.png")
box = cv.imread("../data/images/box.png")

# 初始化BRISK
brisk = cv.BRISK_create()

# 特征关键点检测以及特征描述子计算
keypoints_box_in_scene, descriptors_box_in_scene = brisk.detectAndCompute(box_in_scene, None)
keypoints_box, descriptors_box = brisk.detectAndCompute(box, None)
# keypoints：[keypoint对象，keypoint对象，...，keypoint对象]
# keypoint类属性：(x, y):坐标, size:关键点邻域直径大小, angle:方向, response:检测的响应值, octave:在那一层金字塔检测到的特征点, class_id:对象类别id
# descriptors: (nfeatures, 64)

# 使用汉明距离，暴力一对一匹配
bf = cv.BFMatcher_create(cv.NORM_HAMMING, crossCheck=True)
matches = bf.match(descriptors_box, descriptors_box_in_scene) # 注意这里, 前面是query，后面是train

# 可视化
# 注意这里, 需要与生成match的顺序对应，前面是query，后面是train
result = cv.drawMatches(box, keypoints_box, box_in_scene, keypoints_box_in_scene, matches, None)
cv.imshow("result", result)
cv.waitKey(0)
cv.destroyAllWindows()