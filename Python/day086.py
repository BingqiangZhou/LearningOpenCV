'''
Author       : Bingqiang Zhou
Date         : 2021-08-29 11:52:40
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-29 12:52:11
Description  : 视频分析 – 稠密光流分析
    光流跟踪方法分为稠密光流跟踪与稀疏光流跟踪算法，KLT是稀疏光流跟踪算法，前面我们已经介绍过了，
    OpenCV还支持稠密光流的移动对象跟踪方法，OpenCV中支持的稠密光流算法是由Gunner Farneback在2003年提出来的，
    它是基于前后两帧所有像素点的移动估算算法，其效果要比稀疏光流算法更好，相关的API如下：
    void cv::calcOpticalFlowFarneback(
        InputArray 	prev, // 前一帧
        InputArray 	next, // 后一帧
        InputOutputArray 	flow, // 光流，计算得到的移动能量场
        double 	pyr_scale, // 金字塔放缩比率
        int 	levels, // 金字塔层级数目
        int 	winsize, // 表示窗口大小
        int 	iterations, // 表示迭代次数
        int 	poly_n, // 表示光流生成时候，对邻域像素的多项式展开，n越大越模糊越稳定
        double 	poly_sigma, // 表示光流多项式展开时候用的高斯系数，n越大，sigma应该适当增加
        int 	flags // 有两个OPTFLOW_USE_INITIAL_FLOW(0)表示使用盒子模糊进行初始化光流, OPTFLOW_FARNEBACK_GAUSSIAN(1)表示使用高斯窗口
    )
'''

import cv2 as cv
import numpy as np

capture = cv.VideoCapture("../data/videos/vtest.avi")
success, frame = capture.read()
prev_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

hsv = np.zeros_like(frame) # 色调H，饱和度S，明度V，转到HSV有个好处，背景颜色不会变化，直接转到BGR或出现背景颜色闪烁的情况
hsv[..., 1] = 255
result = np.zeros((frame.shape[0], frame.shape[1]*2, frame.shape[2]), dtype=frame.dtype)

while True:
    success, frame = capture.read()
    if success:
        next_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        flow = cv.calcOpticalFlowFarneback(prev_gray, next_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0) # (h, w, 2)
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1]) # 笛卡尔坐标系转到极坐标系，角度指范围在[0，2*Pi]
        hsv[..., 0] = ang*180/np.pi/2
        hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
        bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        result[:, :frame.shape[1],:] = frame
        result[:, frame.shape[1]:,:] = bgr
        cv.imshow("result", result)
        key = cv.waitKey(50)
        if key == 27: # ESC
            break
        prev_gray = next_gray
    else:
        break
    # break

cv.destroyAllWindows()
