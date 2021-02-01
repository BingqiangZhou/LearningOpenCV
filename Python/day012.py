'''
Author       : Bingqiang Zhou
Date         : 2021-02-02 02:19:05
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-02 03:31:49
Description  : 视频文件的读写
    视频读写
    VideoCapture 视频文件读取、摄像头读取、视频流读取
    VideoWriter 视频写出、文件保存、
    常用属性
    - CAP_PROP_FRAME_HEIGHT
    - CAP_PROP_FRAME_WIDTH
    - CAP_PROP_FRAME_COUNT
    - CAP_PROP_FPS
    不支持音频编码与解码保存，不是一个音视频处理的库！主要是分析与解析视频内容。保存文件最大支持单个文件为2G
'''

import cv2 as cv

capture = cv.VideoCapture() #初始化VideoCapture对象
capture.open("../data/videos/video.avi") # 打开视频文件，open(0)则打开摄像头(0是deviceID)
# capture = cv.VideoCapture("../data/videos/video.avi", cv.CAP_FFMPEG)

# 常用参数
height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
frames = capture.get(cv.CAP_PROP_FRAME_COUNT)
fps = capture.get(cv.CAP_PROP_FPS)
fourcc = capture.get(cv.CAP_PROP_FOURCC)
print("height: {}, width: {}, frames: {}, fps: {}, fourcc: {}".format(height, width, frames, fps, fourcc))

# 读取video.avi文件，并保存到test.mp4
# 初始化VideoWriter对象writer，
# 其中fourcc参数是用于压缩视频帧的编解码器的4个字符代码，
# fourcc设置为-1，可以弹出选择编解码器的对话框（第一次运行时可以使用-1，来确定本机存在哪些编解码器）
# codec参考：https://www.fourcc.org/codecs.php
# macOS 下可用的codec：https://gist.github.com/takuma7/44f9ecb028ff00e2132e
writer = cv.VideoWriter("../data/videos/test.mp4", cv.VideoWriter_fourcc(*'DIVX'), fps, (int(height), int(width)), True)

while True:
    ret, frame = capture.read() # 循环读取视频帧
    if ret is True: # 判断是否到了文件末尾
        cv.imshow("VideoCapture read video file", frame); # 显示视频帧
        if writer.isOpened():
            writer.write(frame)
        c = cv.waitKey(50) # 每隔50毫秒，对键盘按键事件监听
        if c == 27 :  # 如果按下ESC键（acsii对应27），退出循环读取视频帧
            break
    else:
        break

# 释放资源
writer.release()  
capture.release() 


# 使用摄像头录制视频
camera_capture = cv.VideoCapture(0) # 打开摄像头

camera_writer = cv.VideoWriter()
camera_writer.open("../data/videos/camera.avi", cv.VideoWriter_fourcc(*'MJPG'), 30, (500, 500), True)


while True:
    ret, frame = camera_capture.read()
    if ret is True:
        cv.imshow("i see you!", frame)
        camera_writer.write(frame)
        c = cv.waitKey(50); # 每隔50毫秒，对键盘按键事件监听
        if (c == 27) :  # 如果按下ESC键（acsii对应27），退出循环读取视频帧
            break
    else:
        break

# 释放资源
camera_writer.release()
camera_capture.release()