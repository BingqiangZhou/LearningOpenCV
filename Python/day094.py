'''
Author       : Bingqiang Zhou
Date         : 2021-08-30 10:49:32
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-30 11:26:13
Description  : ORB FAST特征关键点检测
    ORB - (Oriented Fast and Rotated BRIEF)算法是基于FAST特征检测与BRIEF特征描述子匹配实现，
    相比BRIEF算法中依靠随机方式获取而值点对，ORB通过FAST方法，
    FAST方式寻找候选特征点方式是假设灰度图像像素点A周围的像素存在连续大于或者小于A的灰度值，
    选择任意一个像素点P，假设半径为3，周围16个像素表示，则像素点P被标记为候选特征点、通常N取值为9、12，上图N=9。
    为了简化计算，我们可以只计算1、9、5、13四个点，至少其中三个点满足上述不等式条件，即可将P视为候选点。
    然后通过阈值进行最终的筛选即可得到ORB特征点

    static Ptr&lt;ORB&gt; cv::ORB::create	(
        int nfeatures = 500,
        float scaleFactor = 1.2f,
        int nlevels = 8,
        int edgeThreshold = 31,
        int firstLevel = 0,
        int WTA_K = 2,
        ORB::ScoreType 	scoreType = ORB::HARRIS_SCORE,
        int patchSize = 31,
        int fastThreshold = 20 
    )
    nfeatures 最终输出最大特征点数目
    scaleFactor 金字塔上采样比率
    nlevels 金字塔层数
    edgeThreshold 边缘阈值
    firstLevel= 0
    WTA_K这个是跟BRIEF描述子用的
    scoreType 对所有的特征点进行排名用的方法
    
    拓展资料：
        图像特征之ORB特征详解：https://xhy3054.github.io/visual-feature-orb/
        OpenCV中KeyPoint类：https://blog.csdn.net/u010821666/article/details/52883580
'''

import cv2 as cv
import numpy as np

src = cv.imread("../data/images/test1.png")

# 初始化ORB FAST特征关键点检测器
orb = cv.ORB_create(nfeatures=500, scaleFactor=1.2, nlevels=8, edgeThreshold=31, firstLevel=0, 
                    WTA_K=2, scoreType=cv.ORB_HARRIS_SCORE, patchSize=31, fastThreshold=20)

# FAST特征关键点检测
keypoints = orb.detect(src)
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