'''
Author       : Bingqiang Zhou
Date         : 2021-09-03 13:31:38
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-03 15:31:21
Description  : OpenCV DNN 直接调用tensorflow的导出模型
    OpenCV在DNN模块中支持直接调用tensorflow object detection训练导出的模型使用，支持的模型包括
    -	SSD
    -	Faster-RCNN
    -	Mask-RCNN
    三种经典的对象检测网络，这样就可以实现从tensorflow模型训练、导出模型、
    在OpenCV DNN调用模型网络实现自定义对象检测的技术链路，具有非常高的实用价值。

    对于这些模型没有与之匹配的graph.pbtxt文件，OpenCV DNN模块提供python脚本来生成，相关详细说明看这篇文章：
    tensorflow模型导出与OpenCV DNN中使用：https://mp.weixin.qq.com/s/YZeCNjlVKTU6lOVrmYLDCQ
    运行案例见../data/models/pb_to_pbtxt.ipynb
    
    拓展资料：
        OpenCV deep learning module samples：https://github.com/opencv/opencv/tree/master/samples/dnn
        Deep Neural Networks (dnn module)：https://docs.opencv.org/4.5.3/d2/d58/tutorial_table_of_content_dnn.html
        Deep Neural Network module：https://docs.opencv.org/4.5.3/d6/d0f/group__dnn.html
        cv::dnn::Net Class Reference：https://docs.opencv.org/4.5.3/db/d30/classcv_1_1dnn_1_1Net.html
        cv::dnn::Layer Class Reference：https://docs.opencv.org/4.5.3/d3/d6c/classcv_1_1dnn_1_1Layer.html
        TensorFlow 2 Detection Model Zoo：https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md
        TensorFlow 1 Detection Model Zoo：https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md
        https://github.com/tensorflow/models/tree/master/research/object_detection/samples/configs
        Conversion of TensorFlow Classification Models and Launch with OpenCV Python：https://docs.opencv.org/4.5.3/d1/d8f/tf_cls_tutorial_dnn_conversion.html
'''
import cv2 as cv
import numpy as np

model_path = '../data/models/ssd_mobilenet_v2_coco/frozen_inference_graph.pb'
# convert_pb_to_pbtxt(model_path)
txt_path = '../data/models/ssd_mobilenet_v2_coco/graph.pbtxt'

# 加载模型并设置合适的计算后台和计算设备
net = cv.dnn.readNetFromTensorflow(model_path, txt_path)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# 读取图片
img = cv.imread("../data/images/dog.jpg")
h, w = img.shape[:2]
blob = cv.dnn.blobFromImage(img, 1.0, (300, 300), (), swapRB=False, crop=False)

# 预测
net.setInput(blob)
out = net.forward() # (1, 1, 100, 7)
# 最多检测100个对象，7维第一维为属于那张输入图像（一张输入图像则全为0），第二维为对象的id，第三维为分数，
# 第四维到七维为bbox的坐标比率（需要乘以原高宽大小）, [left, top, right, bottom]。
index = np.nonzero(out[0, 0, :, 1]) # 获取检查为对象的index

for i in index[0]:
    object_score = out[0, 0, i, 2] # 获取对象的分数
    left = int(out[0, 0, i, 3] * w)
    top = int(out[0, 0, i, 4] * h)
    right = int(out[0, 0, i, 5] * w)
    bottom = int(out[0, 0, i, 6] * h)
    if object_score > 0.6:
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


