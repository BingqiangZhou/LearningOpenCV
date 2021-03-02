'''
Author       : Bingqiang Zhou
Date         : 2021-03-02 21:25:18
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-03-02 21:51:46
Description  : 视频分析 – 背景消除与前景ROI提取
    通过视频中的背景进行建模，实现背景消除，生成mask图像，
    通过对mask二值图像分析实现对前景活动对象ROI区域的提取，是很多视频监控分析软件常用的手段之一，该方法很实时！
    整个步骤如下：
        1.	初始化背景建模对象GMM
        2.	读取视频一帧
        3.	使用背景建模消除生成mask
        4.	对mask进行轮廓分析提取ROI
        5.	绘制ROI对象
'''

import cv2 as cv

capture = cv.VideoCapture("../data/videos/vtest.avi")

# 1.初始化背景建模对象GMM
fgbg = cv.createBackgroundSubtractorMOG2(
    history=500, varThreshold=1000, detectShadows=False
)

while True:
    # 2.读取视频一帧
    success, frame = capture.read()
    if success:
        # 3.使用背景建模消除生成mask
        mask = fgbg.apply(frame)
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 5))
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel) 
        cv.imshow("mask", mask)

        # 4.对mask进行轮廓分析提取ROI
        contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours)):
            area = cv.contourArea(contours[i])
            if area < 100:
                continue
            # 5.绘制ROI对象
            (y, x), (h, w), angle = cv.minAreaRect(contours[i])
            cv.ellipse(frame, (int(y), int(x)), (int(h/2), int(w/2)), angle, 0, 360, (0, 0, 255))
            cv.circle(frame, (int(y), int(x)), 3, (0, 255, 0), -1)
        
        cv.imshow("result", frame)

        c = cv.waitKey(50)
        if c == 27: # ESC
            break

cv.waitKey(0)
cv.destroyAllWindows()
