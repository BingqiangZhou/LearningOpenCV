'''
Author       : Bingqiang Zhou
Date         : 2021-09-03 12:10:02
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-03 12:34:09
Description  : OpenCV DNN 基于残差网络的人脸检测
    OpenCV在DNN模块中提供了基于残差SSD网络训练的人脸检测模型，该模型分别提供了tensorflow版本，caffe版本，torch版本模型文件，
    其中tensorflow版本的模型做了更加进一步的压缩优化，大小只有2MB左右，非常适合移植到移动端使用，实现人脸检测功能，
    而caffe版本的是fp16的浮点数模型，精准度更好。要先获得这些模型，只要下载OpenCV4.0源码之后，
    打开运行sources\samples\dnn\face_detector\download_weights.py该脚本即可。
    没有对比就没有伤害，同样一张图像，在OpenCV HAAR与LBP级联检测器中必须通过不断调整参数才可以检测出全部人脸，
    而通过使用该模型，基本在Python语言中基于OpenCV后台的推断，在25毫秒均可以检测出结果，网络支持输入size大小为300x300。

    拓展资料：
        OpenCV deep learning module samples：https://github.com/opencv/opencv/tree/master/samples/dnn
        Deep Neural Networks (dnn module)：https://docs.opencv.org/4.5.3/d2/d58/tutorial_table_of_content_dnn.html
        Deep Neural Network module：https://docs.opencv.org/4.5.3/d6/d0f/group__dnn.html
        cv::dnn::Net Class Reference：https://docs.opencv.org/4.5.3/db/d30/classcv_1_1dnn_1_1Net.html
        cv::dnn::Layer Class Reference：https://docs.opencv.org/4.5.3/d3/d6c/classcv_1_1dnn_1_1Layer.html
'''

import cv2 as cv
import numpy as np

model_path = '../data/models/face_detector/opencv_face_detector_uint8.pb'
txt_path = '../data/models/face_detector/opencv_face_detector.pbtxt'

# 加载模型并设置合适的计算后台和计算设备
net = cv.dnn.readNetFromTensorflow(model_path, txt_path)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# 读取图片
img = cv.imread("../data/images/persons.png")
h, w = img.shape[:2]
blob = cv.dnn.blobFromImage(img, 1.0, (300, 300), (), swapRB=False, crop=False)

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
        cv.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
        out_str = f"score: {object_score}"
        cv.putText(img, out_str, (left-5, top-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, 8)

# 获取推理时间、类别等信息
t, timings = net.getPerfProfile() # t为总时间，timings为每一层的时间
use_time = t / cv.getTickFrequency()
print(f"use time {use_time}s")

# 可视化
# cv.putText(img, out_str, (0, 20), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
cv.imshow("result", img)
cv.waitKey(0)
cv.destroyAllWindows()

