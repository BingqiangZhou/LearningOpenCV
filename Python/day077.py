'''
Author       : Bingqiang Zhou
Date         : 2021-03-02 16:28:55
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-03-02 17:01:58
Description  : 视频读写与处理
    OpenCV中对视频内容的处理本质上对读取视频的关键帧进行解析图像，然后对图像进行各种处理，
    OpenCV的VideoCapture是一个视频读取与解码的API接口，支持各种视频格式、网络视频流、摄像头读取。
    正常的视频处理与分析，主要是针对读取到每一帧图像，衡量一个算法处理是否能够满足实时要求的时候通常通过FPS（每秒多少帧的处理能力）。
    一般情况下每秒大于5帧基本上可以认为是在进行视频处理。
'''

import cv2 as cv

# 按‘1’键高斯模糊，按‘2’键取反，按‘3’键Canny边缘提取
def process(image, c):
    # ascii码值参考: http://ascii.911cha.com
    if c == 49: # 1
        image = cv.GaussianBlur(image, (3, 3), 0)
    elif c == 50: # 2
        image = cv.bitwise_not(image)
    elif c == 51: # 3
        image = cv.Canny(image, 0, 255)
    return image

# 开启摄像头
capture = cv.VideoCapture(0) 

# 读取视频相关信息：高、宽、总帧数、每秒的帧数
height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
count = capture.get(cv.CAP_PROP_FRAME_COUNT)
fps = capture.get(cv.CAP_PROP_FPS)

print(f"h: {height}, w: {width}, count: {count}, fps: {fps}")

while True:
    success, frame = capture.read()
    if success is True:
        cv.imshow("video", frame)
        c = cv.waitKey(50) # 每50ms监测一次
        
        image = process(frame, c)
        cv.imshow("prcessed image", image)
        if c == 27: # ESC
            break
        
cv.waitKey(0)
cv.destroyAllWindows()
