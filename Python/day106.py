'''
Author       : Bingqiang Zhou
Date         : 2021-09-01 10:16:29
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-01 10:36:07
Description  : AKAZE特征与描述子
    AKAZE特征提取算法是局部特征描述子算法，可以看成是SIFT算法的改进、采用非线性扩散滤波迭代来提取与构建尺度空间、
    采用与SIFT类似的方法寻找特征点、在描述子生成阶段采用ORB类似的方法生成描述子，但是描述子比ORB多了旋转不变性特征。
    ORB采用LDB方法，AKAZE采用 M-LDB
    
    拓展资料：
        A-KAZE论文研读：https://blog.csdn.net/zcg1942/article/details/84570068
'''

import cv2 as cv

box_in_scene = cv.imread("../data/images/box_in_scene.png")
box = cv.imread("../data/images/box.png")

# 初始化AKAZE
zkaze = cv.AKAZE_create()

# 特征关键点检测以及特征描述子计算
keypoints_box_in_scene, descriptors_box_in_scene = zkaze.detectAndCompute(box_in_scene, None)
keypoints_box, descriptors_box = zkaze.detectAndCompute(box, None)
# keypoints：[keypoint对象，keypoint对象，...，keypoint对象]
# keypoint类属性：(x, y):坐标, size:关键点邻域直径大小, angle:方向, response:检测的响应值, octave:在那一层金字塔检测到的特征点, class_id:对象类别id
# descriptors: (nfeatures, 61)

# 使用汉明距离，暴力一对一匹配
bf = cv.BFMatcher_create(cv.NORM_HAMMING, crossCheck=True)
matches = bf.match(descriptors_box, descriptors_box_in_scene) # 注意这里, 前面是query，后面是train

# 可视化
# 注意这里, 需要与生成match的顺序对应，前面是query，后面是train
result = cv.drawMatches(box, keypoints_box, box_in_scene, keypoints_box_in_scene, matches, None)
cv.imshow("result", result)
cv.waitKey(0)
cv.destroyAllWindows()


