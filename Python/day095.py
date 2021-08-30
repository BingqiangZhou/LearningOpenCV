'''
Author       : Bingqiang Zhou
Date         : 2021-08-30 12:32:49
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-30 16:18:23
Description  : ORB BRIEF特征描述子 匹配
    得到特征点数据之后，根据BRIEF算法就可以建立描述子。
    选择候选特征点周围SxS大小的像素块、随机选择n对像素点。
    其中P(x)是图像模糊处理之后的像素值，原因在于高斯模糊可以抑制噪声影响、提供特征点稳定性，
    在实际代码实现中通常用均值滤波替代高斯滤波以便利用积分图方式加速计算获得更好的性能表现。
    常见滤波时候使用3x3~9x9之间的卷积核。滤波之后，根据上述描述子的生成条件，得到描述子。

    作者论文提到n的取值通常为128、256或者512。
    得到二进制方式的字符串描述子之后，匹配就可以通过XOR方式矩形，计算汉明距离。
    ORB特征提取跟纯BRIEF特征提取相比较，BRIEF方式采用随机点方式得最终描述子、而ORB通过FAST得到特征点然后得到描述子。
    
    拓展资料：
        图像特征之ORB特征详解：https://xhy3054.github.io/visual-feature-orb/
'''

import cv2 as cv

box_in_scene = cv.imread("../data/images/box_in_scene.png")
box = cv.imread("../data/images/box.png")

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
matches = bf.match(descriptors_box, descriptors_box_in_scene) # 注意这里, 前面是query，后面是train

# 可视化
# 注意这里, 需要与生成match的顺序对应，前面是query，后面是train
result = cv.drawMatches(box, keypoints_box, box_in_scene, keypoints_box_in_scene, matches, None)
cv.imshow("result", result)
cv.waitKey(0)
cv.destroyAllWindows()
