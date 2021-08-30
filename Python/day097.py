'''
Author       : Bingqiang Zhou
Date         : 2021-08-30 14:35:52
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-30 16:18:33
Description  : 基于描述子匹配的已知对象定位
    图像特征点检测、描述子生成以后，就可以通过OpenCV提供的描述子匹配算法，得到描述子直接的距离，距离越小的说明是匹配越好的，
    设定一个距离阈值，一般是最大匹配距离的1/5～1/4左右作为阈值，得到所有小于阈值的匹配点，作为输入，通过单应性矩阵，
    获得这两个点所在平面的变换关系H，根据H使用透视变换就可以根据输入的对象图像获得场景图像中对象位置，最终绘制位置即可。

    拓展资料：
        OpenCV官方教程 Feature Matching + Homography to find Objects: https://docs.opencv.org/4.5.3/d1/de0/tutorial_py_feature_homography.html
'''

import cv2 as cv
import numpy as np

box_in_scene = cv.imread("../data/images/box_in_scene.png")
box = cv.imread("../data/images/box.png")

# 初始化ORB
orb = cv.ORB_create()

# FAST特征关键点检测以及计算BRIEF特征描述子
keypoints_box_in_scene, descriptors_box_in_scene = orb.detectAndCompute(box_in_scene, None)
keypoints_box, descriptors_box = orb.detectAndCompute(box, None)
# keypoints：[keypoint对象，keypoint对象，...，keypoint对象]
# keypoint类属性：(x, y):坐标, size:关键点邻域直径大小, angle:方向, response:检测的响应值, octave:在那一层金字塔检测到的特征点, class_id:对象类别id
# descriptors: (nfeatures, 32)

# 使用FLANN匹配
FLANN_INDEX_LSH = 6
index_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 12, # 6
                   key_size = 20,     # 12
                   multi_probe_level = 2) #1
flann = cv.FlannBasedMatcher(index_params)
matches = flann.match(descriptors_box, descriptors_box_in_scene, None) # 注意这里, 前面是query，后面是train

# 选取较好的匹配，距离小于最大距离的0.4倍
max_dist = max(matches, key=lambda x: x.distance).distance
good_matches = list(filter(lambda x: x.distance < max_dist*0.4, matches))
# print(len(good_matches))

object_pts = np.float32([ keypoints_box[m.queryIdx].pt for m in good_matches ]).reshape(-1,1,2)
scene_pts = np.float32([keypoints_box_in_scene[m.trainIdx].pt for m in good_matches ]).reshape(-1,1,2)

H, mask = cv.findHomography(object_pts, scene_pts, cv.RANSAC, 5.0)
# H, mask = cv.findHomography(object_pts, scene_pts, cv.RHO)
h, w, d = box.shape
pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
dst = np.int32(cv.perspectiveTransform(pts, H))

# 可视化
box_in_scene = cv.polylines(box_in_scene, [np.int32(dst)], True, (0, 255, 0), 3, cv.LINE_AA)
# 注意这里, 需要与生成match的顺序对应，前面是query，后面是train
result = cv.drawMatches(box, keypoints_box, box_in_scene, keypoints_box_in_scene, good_matches, None)
cv.imshow("result", result)
cv.waitKey(0)
cv.destroyAllWindows()
