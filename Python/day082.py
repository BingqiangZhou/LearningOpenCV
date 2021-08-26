'''
Author       : Bingqiang Zhou
Date         : 2021-08-26 22:56:07
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-26 23:40:43
Description  : 角点检测 – shi-tomas角点检测
    Harris角点检测是一种计算速度很慢的角点检测算法，很难实时计算，所有最常用的是shi-tomas角点检测算法，它的运行速度很快。
    OpenCV中相关API与解释如下：
    void cv::goodFeaturesToTrack(
        InputArray image,
        OutputArray corners,
        int maxCorners,
        double qualityLevel,
        double minDistance,
        InputArray mask = noArray(),
        int blockSize = 3,
        bool useHarrisDetector = false,
        double k = 0.04 
    )
    src单通道输入图像，八位或者浮点数
    corners是输出的关键点坐标集合
    maxCorners表示最大返回关键点数目
    qualityLevel表示拒绝的关键点 R < qualityLevel × max response将会被直接丢弃
    minDistance 表示两个关键点之间的最短距离
    mask 表示mask区域，如果有表明只对mask区域做计算
    blockSize 计算梯度与微分的窗口区域
    useHarrisDetector 表示是否使用harris角点检测，默认是false 为shi-tomas
    k = 0.04默认值，当useHarrisDetector为ture时候起作用
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