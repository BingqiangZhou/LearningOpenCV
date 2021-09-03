'''
Author       : Bingqiang Zhou
Date         : 2021-09-03 10:49:06
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-03 11:33:23
Description  : OpenCV DNN 基于SSD实现对象检测
    OpenCV DNN模块支持常见得对象检测模型SSD， 以及它的移动版Mobile Net-SSD，
    特别是后者在端侧边缘设备上可以实时计算，基于Caffe训练好的mobile-net SSD支持20类别对象检测

    加载网络之后，推断调用的关键API如下：
    Mat cv::dnn::Net::forward(
    const String & 	outputName = String()
    )
    参数缺省值为空

    对对象检测网络来说：
    该API会返回一个四维的tensor，前两个维度是1，后面的两个维度，分别表示检测到BOX数量，以及每个BOX的坐标，对象类别，得分等信息。
    这里需要特别注意的是，这个坐标是浮点数的比率，不是像素值，所以必须转换为像素坐标才可以绘制BOX/矩形。

    拓展资料：
        OpenCV deep learning module samples：https://github.com/opencv/opencv/tree/master/samples/dnn
        Deep Neural Networks (dnn module)：https://docs.opencv.org/4.5.3/d2/d58/tutorial_table_of_content_dnn.html
        Deep Neural Network module：https://docs.opencv.org/4.5.3/d6/d0f/group__dnn.html
        cv::dnn::Net Class Reference：https://docs.opencv.org/4.5.3/db/d30/classcv_1_1dnn_1_1Net.html
        cv::dnn::Layer Class Reference：https://docs.opencv.org/4.5.3/d3/d6c/classcv_1_1dnn_1_1Layer.html
'''

import cv2 as cv
import numpy as np

caffe_model_path = '../data/models/ssd/MobileNetSSD_deploy.caffemodel'
prototxt_path = '../data/models/ssd/MobileNetSSD_deploy.prototxt'
# classes_path = '../data/models/ssd/labelmap_det.txt'
obj_names = ["background",
"aeroplane", "bicycle", "bird", "boat",
"bottle", "bus", "car", "cat", "chair",
"cow", "diningtable", "dog", "horse",
"motorbike", "person", "pottedplant",
"sheep", "sofa", "train", "tvmonitor"]


# 加载模型并设置合适的计算后台和计算设备
net = cv.dnn.readNetFromCaffe(prototxt_path, caffe_model_path)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# 读取图片
img = cv.imread("../data/images/dog.jpg")
h, w = img.shape[:2]
blob = cv.dnn.blobFromImage(img, 0.007, (300, 300), (), swapRB=False, crop=False)

# 预测
net.setInput(blob)
out = net.forward() # (1, 1, 100, 7)
# 最多检测一百个对象，7维第一维为属于那张输入图像（一张输入图像则全为0），第二维为对象的id，第三维为分数，
# 第四维到七维为bbox的坐标比率（需要乘以原高宽大小）, [left, top, right, bottom]。
index = np.nonzero(out[0, 0, :, 1]) # 获取检查为对象的index

for i in index[0]:
    object_name = obj_names[int(out[0, 0, i, 1])] # 获取对象的名称
    object_score = out[0, 0, i, 2] # 获取对象的分数
    left = int(out[0, 0, i, 3] * w)
    top = int(out[0, 0, i, 4] * h)
    right = int(out[0, 0, i, 5] * w)
    bottom = int(out[0, 0, i, 6] * h)
    cv.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
    out_str = f"object: {object_name}, score: {object_score}"
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
