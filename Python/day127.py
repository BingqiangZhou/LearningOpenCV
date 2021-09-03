'''
Author       : Bingqiang Zhou
Date         : 2021-09-03 12:55:42
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-03 13:31:24
Description  : OpenCV DNN 基于残差网络的视频人脸检测
    OpenCV在DNN模块中提供了基于残差SSD网络训练的人脸检测模型，还支持单精度的fp16的检测准确度更好的Caffe模型加载与使用，
    这里实现了一个基于Caffe Model的视频实时人脸监测模型，基于Python与C++代码CPU运行，帧率均可以到达15以上。非常好用。

    拓展资料：
        OpenCV deep learning module samples：https://github.com/opencv/opencv/tree/master/samples/dnn
        Deep Neural Networks (dnn module)：https://docs.opencv.org/4.5.3/d2/d58/tutorial_table_of_content_dnn.html
        Deep Neural Network module：https://docs.opencv.org/4.5.3/d6/d0f/group__dnn.html
        cv::dnn::Net Class Reference：https://docs.opencv.org/4.5.3/db/d30/classcv_1_1dnn_1_1Net.html
        cv::dnn::Layer Class Reference：https://docs.opencv.org/4.5.3/d3/d6c/classcv_1_1dnn_1_1Layer.html
'''

import cv2 as cv
import numpy as np

caffe_model_path = '../data/models/face_detector/res10_300x300_ssd_iter_140000_fp16.caffemodel'
prototxt_path = '../data/models/face_detector/res10_300x300_ssd_iter_140000_fp16_deploy.prototxt'

# 加载模型并设置合适的计算后台和计算设备
net = cv.dnn.readNetFromCaffe(prototxt_path, caffe_model_path)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# 开启摄像头
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read() # 读取视频帧
    if ret is False:
        break

    h, w = frame.shape[:2]
    blob = cv.dnn.blobFromImage(frame, 1.0, (300, 300), (), swapRB=False, crop=False)

    # 预测
    net.setInput(blob)
    out = net.forward() # (1, 1, 200, 7)
    # 最多检测200个对象，7维第一维为属于那张输入图像（一张输入图像则全为0），第二维为对象的id，第三维为分数，
    # 第四维到七维为bbox的坐标比率（需要乘以原高宽大小）, [left, top, right, bottom]。
    index = np.nonzero(out[0, 0, :, 1]) # 获取检查为对象的index

    for i in index[0]:
        object_score = out[0, 0, i, 2] # 获取对象的分数
        left = int(out[0, 0, i, 3] * w)
        top = int(out[0, 0, i, 4] * h)
        right = int(out[0, 0, i, 5] * w)
        bottom = int(out[0, 0, i, 6] * h)
        if object_score > 0.5:
            cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            out_str = f"score: {object_score}"
            cv.putText(frame, out_str, (left-5, top-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, 8)

        # 获取推理时间
        t, timings = net.getPerfProfile() # t为总时间，timings为每一层的时间
        use_time = t / cv.getTickFrequency()
        fps = 1 / use_time
        cv.putText(frame, f'fps: {fps}', (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, 8)
        # print(f"use time {use_time}s, fps {fps}")

    # 可视化
    cv.imshow("result", frame)
    key = cv.waitKey(50)
    if key == 27:
        break

cv.destroyAllWindows()