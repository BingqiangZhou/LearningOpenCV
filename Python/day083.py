'''
Author       : Bingqiang Zhou
Date         : 2021-08-26 23:30:17
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-26 23:40:17
Description  : 角点检测 – 亚像素级别角点检测
    OpenCV中角点检测的结果实际不够精准，因为真实的计算中有些位置可能是在浮点数的空间内才最大值，这样就需要我们通过给定的响应值，
    在像素邻域空间进行拟合，实现亚像素级别的角点检测。OpenCV中相关API与解释如下：
    void cv::cornerSubPix(
        InputArray image,
        InputOutputArray corners,
        Size winSize,
        Size zeroZone,
        TermCriteria criteria 
    )
    image单通道输入图像，八位或者浮点数
    corners是输入输出的关键点坐标集合
    winSize表示插值计算时候窗口大小
    zeroZone表示搜索区域中间的dead region边长的一半，有时用于避免自相关矩阵的奇异性。如果值设为(-1,-1)则表示没有这个区域。
    criteria角点精准化迭代过程的终止条件 (最大迭代的次数以及两次迭代之间值的最小差异)
'''

import cv2 as cv
import numpy as np

def process(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.05, minDistance=10)
    for c in corners:
        x, y = c[0]
        color = np.random.randint(0, 256, (3), dtype=np.int32)
        image = cv.circle(image, (x, y), 5, (int(color[0]), int(color[1]), int(color[2])), 2)
    winSize = (5, 5)
    zeroZone = (-1, -1)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TermCriteria_COUNT, 40, 0.01)
    refined_corners = cv.cornerSubPix(gray, corners, winSize, zeroZone, criteria)
    print(refined_corners)
    for i, c in enumerate(refined_corners):
        print(f"refined corners {i}, {c[0]}") # x, y = c[0]
    return image

capture = cv.VideoCapture("../data/videos/color_object.mp4") 

while True:
    success, frame = capture.read()
    if success is True:
        # cv.imshow("video", frame)
        c = cv.waitKey(50) # 每50ms监测一次
        
        image = process(frame)
        cv.imshow("prcessed image", image)
        if c == 27: # ESC
            break
        
# cv.waitKey(0)
cv.destroyAllWindows()