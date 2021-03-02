'''
Author       : Bingqiang Zhou
Date         : 2021-03-02 16:49:37
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-03-02 21:02:08
Description  : 识别与跟踪视频中的特定颜色对象
    这个是其实图像处理与二值分析的视频版本，通过读取视频每一帧的图像，然后对图像二值分析，得到指定的色块区域，
    主要步骤如下：
        1.	色彩转换BGR2HSV
        2.	inRange提取颜色区域mask
        3.	对mask区域进行二值分析得到位置与轮廓信息
        4.	绘制外接椭圆与中心位置
        5.	显示结果
    其中涉及到的知识点主要包括图像处理、色彩空间转换、形态学、轮廓分析等。
'''

import cv2 as cv

# HSV基本颜色分量范围，参考: https://blog.csdn.net/Taily_Duan/article/details/51506776
def process(image):
    
    # 1.色彩转换BGR2HSV
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # 2.inRange提取颜色区域mask
    mask = cv.inRange(hsv, (11, 43, 46), (34, 255, 255))


    # 3.对mask区域进行二值分析得到位置与轮廓信息
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (15, 15))
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel) # 开操作去掉小块

    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # 找到最大的轮廓
    index = -1
    max_val = 0
    for i in range(len(contours)):
        # cv.drawContours(image, contours, i, (0, 0, 255))
        area = cv.contourArea(contours[i])
        if area > max_val:
            max_val = area
            index = i
    
    # 4.绘制外接椭圆与中心位置
    if index != -1:
        (y, x), (h, w), angle  = cv.minAreaRect(contours[i])
        image = cv.ellipse(image, (int(y), int(x)), (int(h/2), int(w/2)), angle, 0, 360, (0, 0, 255))
        image = cv.circle(image, (int(y), int(x)), 3, (0, 255, 0), -1)

    return image


capture = cv.VideoCapture("../data/videos/balltest.mp4")

while True:
    success, frame = capture.read()
    if success is True:
        # cv.imshow("video", frame)
        # 5.显示结果
        image = process(frame)
        cv.imshow("result", image)
        c = cv.waitKey(50)
        if c == 27: # ESC
            break
    else:
        break

cv.waitKey(0)
cv.destroyAllWindows()

