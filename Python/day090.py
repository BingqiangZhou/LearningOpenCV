'''
Author       : Bingqiang Zhou
Date         : 2021-08-29 19:58:20
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-29 20:12:13
Description  : 视频分析 –对象移动轨迹绘制
    移动对象分析，我们可以绘制对象运行轨迹曲线，这个主要是根据移动对象窗口轮廓，获取中心位置，
    然后使用中心位置进行绘制即可得到。大致的程序步骤如下：
        1. 初始化路径点数组
        2. 对每帧的预测轮廓提取中心位置添加到路径数组
        3. 绘制路径曲线
'''

import cv2 as cv

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

tracking_path = []

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
    if rotated_rect[0][0] > 0 or rotated_rect[0][1] > 0: # 判断ROI坐标是否在图像内
        tracking_path.append(rotated_rect[0])

    # 可视化
    frame = cv.ellipse(frame, rotated_rect, (0, 255, 0), 2)
    nums_point = len(tracking_path)
    if nums_point >= 2:
        for i in range(nums_point-1):
            cv.line(frame, (int(tracking_path[i][0]), int(tracking_path[i][1])), 
                            (int(tracking_path[i+1][0]), int(tracking_path[i+1][1])), (0, 0, 255), 2)
    
    cv.imshow("CamShift", frame)
    # cv.imshow("dst", dst)

    key = cv.waitKey(50)
    if key == 27:
        break

cv.destroyAllWindows()
cap.release()
