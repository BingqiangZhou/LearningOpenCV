'''
Author       : Bingqiang Zhou
Date         : 2021-08-28 22:25:40
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-29 00:03:16
Description  : 视频分析KLT光流跟踪02 - 删除静止点与绘制跟踪轨迹
    光流跟踪方法分为稠密光流跟踪与稀疏光流跟踪算法，KLT是稀疏光流跟踪算法，
    这个算法最早是由Bruce D. Lucas and Takeo Kanade两位作者提出来的，所以又被称为KLT。
    稀疏光流算法工作有三个假设前提条件：
        - 亮度恒定
        - 短距离移动
        - 空间一致性

    OpenCV中KLT算法API及其参数解释如下：
    void cv::calcOpticalFlowPyrLK(
        InputArray 	prevImg, // 前一帧图像
        InputArray 	nextImg, // 后一帧图像
        InputArray 	prevPts, // 前一帧的稀疏光流点
        InputOutputArray 	nextPts, // 后一帧光流点
        OutputArray 	status, // 输出状态，1 表示正常该点保留，否则丢弃
        OutputArray 	err, // 表示错误
        Size winSize = Size(21, 21), // 光流法对象窗口大小
        int maxLevel = 3, // 金字塔层数，0表示只检测当前图像，不构建金字塔图像
        TermCriteria 	criteria = TermCriteria(TermCriteria::COUNT+TermCriteria::EPS, 30, 0.01), // 窗口搜索时候停止条件
        int flags = 0, // 操作标志
        double 	minEigThreshold = 1e-4 // 最小特征值响应，低于最小值不做处理
    )

    在84的知识点分享中我们已经可以跟踪到前后两帧之前的位置移动，但是这个还不足够，
    我们需要绘制移动对象从初始到最终的完整可以检测的运动轨迹，同时对一些静止的角点进行删除，
    所以我们需要对状态为1的角点，计算它们之间的距离，只有dx+dy>min_dist（dx=abs(p1.x –p2.x), dy=abs(p1.y-p2.y)）的我们才对它进行保留跟踪。
'''

import cv2 as cv
import numpy as np

# capture = cv.VideoCapture("../data/videos/vtest.avi") 
capture = cv.VideoCapture("../data/videos/color_object.mp4")

# 读取第一帧并获取第一帧的角点作为关键点用于跟踪
success, frame = capture.read()
pre_frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
corners = cv.goodFeaturesToTrack(pre_frame_gray, maxCorners=500, qualityLevel=0.01, minDistance=10, useHarrisDetector=False)

# cornerSubPix参数
params = dict(
    winSize = (5, 5),
    zeroZone = (-1, -1),
    criteria = (cv.TERM_CRITERIA_EPS + cv.TermCriteria_COUNT, 40, 0.01)
)
feature_points = cv.cornerSubPix(pre_frame_gray, corners, **params)

# calcOpticalFlowPyrLK参数
klt_params = dict(
    winSize = (21, 21), #光流法对象窗口大小
    maxLevel = 3,      # 金字塔层数，0表示只检测当前图像，不构建金字塔图像
    criteria = (cv.TermCriteria_COUNT + cv.TermCriteria_EPS, 30, 0.01), #窗口搜索时候停止条件
    flags = 0,        #操作标志
    minEigThreshold = 1e-4, # 最小特征值响应，低于最小值不做处理
)

min_dist = 2
min_nums_point = 20

while True:
    success, frame = capture.read()
    if success is True:
        pts0 = feature_points.copy()
        next_frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # 移动对象的KLT光流跟踪算法
        pts1, status, err = cv.calcOpticalFlowPyrLK(pre_frame_gray, next_frame_gray, pts0, None, **klt_params)

        # 可视化
        no_feature_indexs =[]
        for i, (p0, p1) in enumerate(zip(pts0, pts1)):
            if status[i][0] == 1 and (abs(p0[0][0] - p1[0][0]) + abs(p0[0][1] - p1[0][1])) > min_dist:
                # print(feature_points.shape, pts0.shape, pts1.shape, p1.shape)
                # feature_points[i, :, :] = p1
                p0 = (p0[0][0], p0[0][1])
                p1 = (p1[0][0], p1[0][1])
                color = np.random.randint(0, 256, (3), dtype=np.int32).tolist()
                frame = cv.circle(frame, p0, 3, color, 2)
                frame = cv.circle(frame, p1, 3,color, 2)
                frame = cv.line(frame, p0, p1, color, 2)
            else:
                no_feature_indexs.append(i)
        if len(no_feature_indexs) > 0:
            feature_points = np.delete(feature_points, no_feature_indexs, axis=0)
        pre_frame_gray = next_frame_gray.copy()
        # 特征点小于`min_nums_point`，进行初始化（特征点检查）
        if len(feature_points) < min_nums_point:
            pre_frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            corners = cv.goodFeaturesToTrack(pre_frame_gray, maxCorners=100, qualityLevel=0.05, minDistance=10, useHarrisDetector=False)
            feature_points = cv.cornerSubPix(pre_frame_gray, corners, **params)
        cv.imshow("prcessed image", frame)
        c = cv.waitKey(50) # 每50ms监测一次
        if c == 27: # ESC
            break
    else:
        break
        
# cv.waitKey(0)
cv.destroyAllWindows()
