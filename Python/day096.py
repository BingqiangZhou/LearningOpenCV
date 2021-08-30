'''
Author       : Bingqiang Zhou
Date         : 2021-08-30 13:31:43
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-30 16:18:51
Description  : 描述子匹配
    图像特征检测首先会获取关键点，然后根据关键点周围像素ROI区域的大小，生成描述子，
    完整的描述子向量就表示了一张图像的特征，是图像特征数据，这种方式也被称为图像特征工程，
    即通过先验模型与合理计算得到图像特征数据的过程，有了特征数据我们就可以利用特征数据实现对象检测与对象识别，
    这个最简单一个方法就是特征匹配，OpenCV提供了两种图像特征匹配的算法
        - 暴力匹配
        - FLANN匹配
    其中FLANN是一种高效的数值或者字符串匹配算法，SIFT/SURF是基于浮点数的匹配，ORB是二值匹配，速度更快。
    对于FLANN匹配算法，当使用ORB匹配算法的时候，需要重新构造HASH。
    对匹配之后的输出结果，根据距离进行排序，就会得到距离比较的匹配点，这个才是好的特征匹配。
    拓展资料：
        OpenCV官方教程 Feature Matching: https://docs.opencv.org/4.5.3/dc/dc3/tutorial_py_matcher.html
        opencv-api FlannBasedMatcher: https://blog.csdn.net/claroja/article/details/83411108
'''

import cv2 as cv

box = cv.imread("../data/images/box.png") # query
box_in_scene = cv.imread("../data/images/box_in_scene.png") # train

# 初始化ORB
orb = cv.ORB_create(nfeatures=500, scaleFactor=1.2, nlevels=8, edgeThreshold=31, firstLevel=0, 
                    WTA_K=2, scoreType=cv.ORB_HARRIS_SCORE, patchSize=31, fastThreshold=20)

# FAST特征关键点检测以及计算BRIEF特征描述子
keypoints_box_in_scene, descriptors_box_in_scene = orb.detectAndCompute(box_in_scene, None)
keypoints_box, descriptors_box = orb.detectAndCompute(box, None)
# keypoints：[keypoint对象，keypoint对象，...，keypoint对象]
# keypoint类属性：(x, y):坐标, size:关键点邻域直径大小, angle:方向, response:检测的响应值, octave:在那一层金字塔检测到的特征点, class_id:对象类别id
# descriptors: (nfeatures, 32)

# 使用汉明距离，暴力一对一匹配
bf = cv.BFMatcher_create(cv.NORM_HAMMING, crossCheck=True)
bf_matches = bf.match(descriptors_box, descriptors_box_in_scene) # 注意这里, 前面是query，后面是train
bf_good_matches = sorted(bf_matches, key=lambda x: x.distance)[:10] # 取距离最小的10个，即匹配度最高的

# 使用FLANN匹配
FLANN_INDEX_LSH = 6
index_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 6, # 12
                   key_size = 12,     # 20
                   multi_probe_level = 1) #2
flann = cv.FlannBasedMatcher(index_params)
flann_matches = flann.match(descriptors_box, descriptors_box_in_scene, None)
flann_good_matches = sorted(flann_matches, key=lambda x: x.distance)[:10] # 取距离最小的10个，即匹配度最高的

# 可视化
# 注意这里, 需要与生成match的顺序对应，前面是query，后面是train
bf_result = cv.drawMatches(box, keypoints_box, box_in_scene, keypoints_box_in_scene, bf_good_matches, None)
cv.imshow("BFMatcher", bf_result)
flann_result = cv.drawMatches(box, keypoints_box, box_in_scene, keypoints_box_in_scene, flann_good_matches, None)
cv.imshow("FlannBasedMatcher", flann_result)
cv.waitKey(0)
cv.destroyAllWindows()

