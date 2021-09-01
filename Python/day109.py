'''
Author       : Bingqiang Zhou
Date         : 2021-09-01 11:37:51
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-01 12:43:55
    Description  : BLOB特征分析 – SimpleBlobDetector使用
    BLOB（斑点）是图像中灰度块的一种专业称呼，更加变通一点的可以说它跟我们前面二值图像分析的联通组件类似，
    通过特征提取中的SimpleBlobDetector可以实现常见的各种灰度BLOB对象组件检测与分离。
    使用该检测器的时候，可以根据需要输入不同参数，得到的结果跟输入的参数息息相关。常见的BLOB分析支持如下：
    -	根据BLOB面积过滤
    -	根据灰度/颜色值过滤
    -	根据圆度过滤
    -	根据长轴与短轴过滤
    -	根据凹凸进行过滤

    参数列表:
    SimpleBlobDetector::Params::Params()
    bool 	filterByArea
    bool 	filterByCircularity
    bool 	filterByColor
    bool 	filterByConvexity
    bool 	filterByInertia
    float 	maxArea
    float 	maxCircularity
    float 	maxConvexity
    float 	maxInertiaRatio
    float 	maxThreshold
    float 	minArea
    float 	minCircularity
    float 	minConvexity
    float 	minDistBetweenBlobs
    float 	minInertiaRatio

    拓展资料：
        OpenCV中blob的概念以及OpenCV中BLOB特征提取与几何形状分类：https://blog.csdn.net/weixin_41010198/article/details/88419862
        opencv SimpleBlobDetector filterByInertia是什么意思？：https://www.coder.work/article/2083807
        官方文档：
            cv::SimpleBlobDetector Class Reference：https://docs.opencv.org/4.5.3/d0/d7a/classcv_1_1SimpleBlobDetector.html
            cv::SimpleBlobDetector::Params Struct Reference：https://docs.opencv.org/4.5.3/d8/da7/structcv_1_1SimpleBlobDetector_1_1Params.html
'''

import cv2 as cv

img = cv.imread("../data/images/zhifang_ball.png")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 设置Blob检测参数：BlobDetector_Params
params = cv.SimpleBlobDetector_Params()
# 根据BLOB面积过滤
params.filterByArea = True
# params.maxArea = 100
params.minArea = 10
# 根据灰度/颜色值过滤
params.filterByColor = True
params.maxThreshold = 256
params.minThreshold = 0
# 根据圆度过滤 ((4*pi*Area) / (perimeter*perimeter(周长)))
params.filterByCircularity = True
# params.maxCircularity = 1
params.minCircularity = 0.1
# 根据凹凸进行过滤 (area / area of blob convex hull)
params.filterByConvexity = True
# params.maxConvexity = 1
params.minConvexity = 0.5
# 根据长轴与短轴过滤
params.filterByInertia = True
# params.maxInertiaRatio = 1
params.minInertiaRatio = 0.5

blob_detector = cv.SimpleBlobDetector_create(params)
keypoints = blob_detector.detect(gray, None)
# 这里需要注意的是flag需要设置为DRAW_RICH_KEYPOINTS
img = cv.drawKeypoints(img, keypoints, None, flags=cv.DrawMatchesFlags_DRAW_RICH_KEYPOINTS) 
cv.imshow("result", img)
cv.waitKey(0)
cv.destroyAllWindows()
