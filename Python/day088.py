'''
Author       : Bingqiang Zhou
Date         : 2021-08-29 18:03:07
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-29 19:06:43
Description  : 视频分析 – 基于均值迁移的对象移动分析
    均值迁移移动对象分析，主要是基于直方图分布与反向投影实现移动对象的轨迹跟踪，
    其核心的思想是对反向投影之后的图像做均值迁移（meanshift）从而发现密度最高的区域，也是对象分布最大的区域。
    完整的算法流程如下：
        1，	读取图像一帧
        2，	HSV直方图
        3，	反向投影该帧
        4，	使用means shift寻找最大分布密度
        5，	更新窗口直至最后一帧
    OpenCV中meanshift的API函数如下：
    int cv::meanShift(
        InputArray probImage,
        Rect & 	window,
        TermCriteria criteria 
    )
    probImage输入图像，是直方图反向投影的结果
    window 搜索窗口，ROI对象区域
    criteria 均值迁移停止条件
'''

import cv2 as cv
import numpy as np

cap =  cv.VideoCapture("../data/videos/balltest.mp4") 
success, frame = cap.read()
cv.namedWindow("meanShift", cv.WINDOW_AUTOSIZE)
x, y, w, h = cv.selectROI("meanShift", frame, showCrosshair=True, fromCenter=False) # 打开一个窗口对小球进行交互
print("select [x, y, w, h]: ", x, y, w, h)
track_window = (x, y, w, h)

roi = frame[x:x+w, y:y+h]
hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV) # 将颜色空间转到HSV，利用色调H的直方图来做反向映射（小球的颜色为黄色，利用色调来做，能得到更好的效果）
mask = cv.inRange(hsv_roi, (26, 43, 46), (34, 255, 255)) # 在视频中，小球的颜色为黄色，将黄色部分的内容提取出来便于追逐
roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX) # normlize到[0, 255]

while True:
    success, frame = cap.read()
    if not success:
        break
    
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # 反向投影该帧
    dst = cv.calcBackProject([hsv_frame], [0], roi_hist, [0, 180], 1)

    # 使用means shift寻找最大分布密度
    ret, track_window = cv.meanShift(dst, track_window, criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1))
    # print(track_window)
    
    # 可视化
    frame = cv.rectangle(frame, track_window, (0, 255, 0), 2)
    
    cv.imshow("meanShift", frame)
    # cv.imshow("dst", dst)

    key = cv.waitKey(50)
    if key == 27:
        break

cv.destroyAllWindows()
cap.release()

