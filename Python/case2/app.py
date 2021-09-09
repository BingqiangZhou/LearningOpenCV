'''
Author       : Bingqiang Zhou
Date         : 2021-09-09 14:33:45
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-09 16:33:59
Description  : 案例二 - 车道线检测
    算法基本思想说明：
    传统的车道线检测，多数是基于霍夫直线检测，其实这个里面有个很大的误区，
    霍夫直线拟合容易受到各种噪声干扰，直接运用有时候效果不好，更多的时候通过霍夫直线检测进行初步的筛选，
    然后再有针对性的进行直线拟合，根据拟合的直线四个点坐标，绘制出车道线，
    这种方式可以有效避免霍夫直线拟合不良后果，是一种更加稳定的车道线检测方法，
    在实际项目中，可以选择两种方法并行，在计算出结果后进行叠加或者对比提取，
    
    今天分享的案例主要是绕开了霍夫直线检测，通过对二值图像进行轮廓分析与几何分析，
    提取到相关的车道线信息、然后进行特定区域的像素扫描，拟合生成直线方程，
    确定四个点绘制出车道线，对连续的视频来说，如果某一帧无法正常检测，就可以通过缓存来替代绘制，
    从而实现在视频车道线检测中实时可靠。

    PS: 当前深度学习基于FCN与Mask-R-CNN实现像素级别的图像分割，对车道线检测有很大的借鉴意义。
'''

import cv2 as cv

def process(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    h, w = gray.shape
    binary = cv.Canny(gray, 150, 300)
    binary[0:int(h/2+40), 0:w] = 0 # 去掉图像上半部分边缘的干扰
    contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        area = cv.contourArea(contours[i]) # 面积
        l = cv.arcLength(contours[i], True) # 周长
        (x, y), (a, b), angle = cv.minAreaRect(contours[i]) # 角度
        angle = abs(angle)
        if l < 10 or area < 20: # 去掉面积与周长较小的边缘
            continue
        if y > (h - 50): # 去掉视频右下方的日期
            continue
        if angle < 20 or angle > 160 or angle == 90:
            continue
        [vx, vy, x, y] = cv.fitLine(contours[i], cv.DIST_L1, 0, 0.01, 0.01)
        # print(vx, vy, x, y)
        k = vy / vx
        if 1e-3 < abs(k) < 1e3:
            c = y - k * x
            dy = k * b + c
            y2 = y + dy
            x2 = (y2 - c) / k
            cv.line(image, (x, y), (x2, y2), (0, 255, 0), 2, 8)
            # lines.append([(x, y), (x2, y2)])

        # cv.drawContours(image, contours, i, (0, 0, 255), 2, 8)
    return image

cap = cv.VideoCapture("./videos/road_line.mp4")

while True:
    ret, frame = cap.read()
    if ret is False:
        break
    
    frame = process(frame)

    k = cv.waitKey(50)
    cv.imshow("frame", frame)
    if k == 27:
        break

cv.destroyAllWindows()