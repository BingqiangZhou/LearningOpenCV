'''
Author       : Bingqiang Zhou
Date         : 2021-08-28 18:43:17
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-28 19:23:20
Description  : 视频分析 - 移动对象的KLT光流跟踪算法
    光流跟踪方法分为稠密光流跟踪与稀疏光流跟踪算法，KLT是稀疏光流跟踪算法，
    这个算法最早是由Bruce D. Lucas and Takeo Kanade两位作者提出来的，所以又被称为KLT。
    稀疏光流算法工作有三个假设前提条件：
        -亮度恒定
        -短距离移动
        -空间一致性

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
'''

import cv2 as cv
import numpy as np

capture = cv.VideoCapture("../data/videos/vtest.avi") 

# 读取第一帧并获取第一帧的角点作为关键点用于跟踪
success, frame = capture.read()
pre_frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
corners = cv.goodFeaturesToTrack(pre_frame_gray, maxCorners=100, qualityLevel=0.05, minDistance=10)

# cornerSubPix参数
params = dict(
    winSize = (5, 5),
    zeroZone = (-1, -1),
    criteria = (cv.TERM_CRITERIA_EPS + cv.TermCriteria_COUNT, 40, 0.01)
)
pts0 = cv.cornerSubPix(pre_frame_gray, corners, **params)

# calcOpticalFlowPyrLK参数
klt_params = dict(
    winSize = (21, 21), #光流法对象窗口大小
    maxLevel = 3,      # 金字塔层数，0表示只检测当前图像，不构建金字塔图像
    criteria = (cv.TermCriteria_COUNT + cv.TermCriteria_EPS, 30, 0.01), #窗口搜索时候停止条件
    flags = 0,        #操作标志
    minEigThreshold = 1e-4, # 最小特征值响应，低于最小值不做处理
)

while True:
    success, frame = capture.read()
    if success is True:
        next_frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # 移动对象的KLT光流跟踪算法
        pts1, status, err = cv.calcOpticalFlowPyrLK(pre_frame_gray, next_frame_gray, pts0, None, **klt_params)
        
        # 根据状态确定保留的点
        pts_old = pts0[status == 1]
        pts_new = pts1[status == 1]

        # 可视化
        for i, (p0, p1) in enumerate(zip(pts_old, pts_new)):
            # print(p0, p1)
            p0 = (p0[0], p0[1])
            p1 = (p1[0], p1[1])
            color = np.random.randint(0, 256, (3), dtype=np.int32).tolist()
            frame = cv.circle(frame, p0, 5, color, 2)
            frame = cv.circle(frame, p1, 5,color, 2)
            frame = cv.line(frame, p0, p1, color, 2)
        pre_frame_gray = next_frame_gray.copy()
        pts0 = pts1
        cv.imshow("prcessed image", frame)
        c = cv.waitKey(50) # 每50ms监测一次
        if c == 27: # ESC
            break
    else:
        break
        
# cv.waitKey(0)
cv.destroyAllWindows()
