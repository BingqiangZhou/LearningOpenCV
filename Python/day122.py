'''
Author       : Bingqiang Zhou
Date         : 2021-09-02 23:20:49
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-02 23:59:47
Description  : OpenCV DNN 实现图像分类

    使用ImageNet数据集支持1000分类的GoogleNet网络模型， 分别演示了Python与C++语言中的使用该模型实现图像分类标签预测。其中label标签是在一个单独的文本文件中读取，模型从上面的链接中下载即可。读取模型的API：
    Net cv::dnn::readNetFromCaffe(
        const String & 	prototxt,
        const String & 	caffeModel = String() 
    )
    prototxt表示模型的配置文件
    caffeModel表示模型的权重二进制文件

    使用模型实现预测的时候，需要读取图像作为输入，网络模型支持的输入数据是四维的输入，所以要把读取到的Mat对象转换为四维张量，OpenCV的提供的API为如下：
    Mat cv::dnn::blobFromImage(
        InputArray 	image,
        double 	scalefactor = 1.0,
        const Size & 	size = Size(),
        const Scalar & 	mean = Scalar(),
        bool 	swapRB = false,
        bool 	crop = false,
        int 	ddepth = CV_32F 
    )
    image输入图像
    scalefactor 默认1.0
    size表示网络接受的数据大小
    mean表示训练时数据集的均值
    swapRB 是否互换Red与Blur通道
    crop剪切
    ddepth 数据类型

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

# 加载模型
net = cv.dnn.readNetFromCaffe(prototxt_path, caffe_model_path)

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
