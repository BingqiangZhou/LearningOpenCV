'''
Author       : Bingqiang Zhou
Date         : 2021-08-29 19:27:48
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-29 19:41:05
Description  : 视频分析 – 基于连续自适应均值迁移（CAM）的对象移动分析
    CAM是连续自适应的均值迁移跟踪算法，它跟均值迁移相比较有两个改进
        - 会根据跟踪对象大小变化自动调整搜索窗口大小
        - 返回位置信息更加完整，包含了位置与角度信息
    OpenCV中CAMShift的API函数如下：
    RotatedRect cv::CamShift(
        InputArray probImage,
        Rect & 	window,
        TermCriteria criteria 
    )
    probImage输入图像，是直方图反向投影的结果
    window 搜索窗口，ROI对象区域
    criteria 均值迁移停止条件

    特别需要注意的是：
    C++版本中会自动更新搜索窗口，
    Python语言版本中必须每次从返回信息中手动更新。
'''

import cv2 as cv
import numpy as np

cap =  cv.VideoCapture("../data/videos/balltest.mp4") 
success, frame = cap.read()
cv.namedWindow("CamShift", cv.WINDOW_AUTOSIZE)
x, y, w, h = cv.selectROI("CamShift", frame, showCrosshair=True, fromCenter=False) # 打开一个窗口对小球进行交互
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

    # 使用CamShift寻找最大分布密度
    track_box = cv.CamShift(dst, track_window, criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1))
    # track_box (RotatedRect, Rect) ((center_x, center_y), (w, h), angle), (left_x, left_y, w, h))
    # print(track_box)
    rotated_rect = track_box[0]
    track_window = track_box[1]

    # 可视化
    frame = cv.ellipse(frame, rotated_rect, (0, 255, 0), 2)
    
    cv.imshow("CamShift", frame)
    # cv.imshow("dst", dst)

    key = cv.waitKey(50)
    if key == 27:
        break

cv.destroyAllWindows()
cap.release()


