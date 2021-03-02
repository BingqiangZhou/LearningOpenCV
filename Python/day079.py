'''
Author       : Bingqiang Zhou
Date         : 2021-03-02 18:58:59
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-03-02 21:21:04
Description  : 视频分析 - 背景/前景 提取 
    视频场景分析中最常用的技术之一就是通过背景消除来提取前景移动对象，得到前景的对象mask图像，
    最常用的背景消除技术就是通过帧差相减，用前面一帧作为背景图像，与当前帧进行相减，
    不过这种方法对光照与噪声影响非常敏感，所有好的办法是通过对前面一系列帧提取背景模型进行相减，
    OpenCV中实现的背景模型提取算法有两种，
        一种是基于高斯混合模型GMM实现的背景提取，
        另外一种是基于最近邻KNN实现的。
    都有相关的API可以供开发者使用。相关API
    Ptr<BackgroundSubtractorMOG2> cv::createBackgroundSubtractorMOG2(
        int  history = 500, 
        double 	varThreshold = 16,
        bool  detectShadows = true 
    )
    参数解释如下：
    history表示过往帧数，500帧，选择history = 1就变成两帧差
    varThreshold表示像素与模型之间的马氏距离，值越大，只有那些最新的像素会被归到前景，值越小前景对光照越敏感。
    detectShadows 是否保留阴影检测，请选择False这样速度快点。

    GMM：
        Ptr<BackgroundSubtractor> pBackSub = createBackgroundSubtractorMOG2();
        原理参考：https://www.cnblogs.com/my-love-is-python/p/10440827.html
    KNN：
        Ptr<BackgroundSubtractor> pBackSub = createBackgroundSubtractorKNN();
        原理参考：
    
    官方文档：https://docs.opencv.org/4.5.1/de/de1/group__video__motion.html#gac9be925771f805b6fdb614ec2292006d
'''

import cv2 as cv

capture = cv.VideoCapture("../data/videos/color_object.mp4")

fgbg = cv.createBackgroundSubtractorMOG2(
    history=500, varThreshold=1000, detectShadows=False
)

# KNN 效果没有 GMM好
# fgbg = cv.createBackgroundSubtractorKNN(
#     history=500, dist2Threshold=100, detectShadows=False
# )

while True:
    success, frame = capture.read()
    if success is True:
        fgmask = fgbg.apply(frame)
        background = fgbg.getBackgroundImage()
        cv.imshow("video", frame)
        cv.imshow('mask', fgmask)
        cv.imshow("background", background)
        c = cv.waitKey(30)
        if c == 27: # ESC
            break
    else:
        break

cv.waitKey(0)
cv.destroyAllWindows()
