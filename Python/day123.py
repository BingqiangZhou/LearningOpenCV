'''
Author       : Bingqiang Zhou
Date         : 2021-09-03 00:04:23
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-03 00:15:45
Description  : OpenCV DNN 为模型运行设置目标设备与计算后台
    OpenCV中加载网络模型之后，可以设置计算后台与计算目标设备，OpenCV DNN模块支持这两个设置的相关API如下：
    cv::dnn::Net::setPreferableBackend(
        int backendId
    )
    backendId 表示后台计算id，
    - DNN_BACKEND_DEFAULT (DNN_BACKEND_INFERENCE_ENGINE)表示默认使用intel的预测推断库
        (需要下载安装Intel® OpenVINO™ toolkit， 然后重新编译OpenCV源码，在CMake时候enable该选项方可)， 可加速计算！
    - DNN_BACKEND_OPENCV 一般情况都是使用opencv dnn作为后台计算，
    - DNN_BACKEND_CUDA  使用CUDA做后台计算

    void cv::dnn::Net::setPreferableTarget(
        int targetId
    )
    常见的目标设备id如下：
    - DNN_TARGET_CPU其中表示使用CPU计算，默认是的
    - DNN_TARGET_OPENCL 表示使用OpenCL加速，一般情况速度都很扯
    - DNN_TARGET_OPENCL_FP16 可以尝试
    - DNN_TARGET_MYRIAD 树莓派上的
    - DNN_TARGET_CUDA, 使用CUDA加速
    - DNN_TARGET_CUDA_FP16, 使用CUDA、fp16精度的浮点数
    
    拓展资料：
        OpenCV deep learning module samples：https://github.com/opencv/opencv/tree/master/samples/dnn
        Deep Neural Networks (dnn module)：https://docs.opencv.org/4.5.3/d2/d58/tutorial_table_of_content_dnn.html
        Deep Neural Network module：https://docs.opencv.org/4.5.3/d6/d0f/group__dnn.html
        cv::dnn::Net Class Reference：https://docs.opencv.org/4.5.3/db/d30/classcv_1_1dnn_1_1Net.html
        cv::dnn::Layer Class Reference：https://docs.opencv.org/4.5.3/d3/d6c/classcv_1_1dnn_1_1Layer.html
'''

import cv2 as cv
import numpy as np

caffe_model_path = '../data/models/googlenet/bvlc_googlenet.caffemodel'
prototxt_path = '../data/models/googlenet/bvlc_googlenet.prototxt'
classes_path = '../data/models/googlenet/classification_classes_ILSVRC2012.txt'

# 对于分类类别
with open(classes_path, 'r') as f:
    classes = [ s.strip() for s in f.readlines()]
    # print(classes)


# 加载模型并设置合适的计算后台和计算设备
net = cv.dnn.readNetFromCaffe(prototxt_path, caffe_model_path)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# 读取图片
img = cv.imread("../data/images/flower.png")
img = cv.resize(img, (224, 224))
blob = cv.dnn.blobFromImage(img, 1.0, (224, 224), (), swapRB=False, crop=False)

# 预测
net.setInput(blob)
out = net.forward() # (1, 1000)
out = out.flatten()
# softmax = lambda x: np.exp(x)/sum(np.exp(x))
# out = softmax(out)

# 获取推理时间、类别等信息
t, timings = net.getPerfProfile()
use_time = t / cv.getTickFrequency()
index = np.argmax(out)
out_str = f'class: {classes[index]}, confidence: {out[index]}, use time {use_time}s'
print(out_str)

# 可视化
cv.putText(img, out_str, (0, 20), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
cv.imshow("result", img)
cv.waitKey(0)
cv.destroyAllWindows()

