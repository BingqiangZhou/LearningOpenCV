'''
Author       : Bingqiang Zhou
Date         : 2021-09-02 22:45:50
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-02 23:25:41
Description  : OpenCV DNN 获取导入模型各层信息
    googlenet 模型支持1000个类别的图像分类，OpenCV DNN模块支持下面框架的预训练模型的前馈网络(预测图)使用
    -	Caffe
    -	Tensorflow
    -	Torch
    -	DLDT
    -	Darknet

    同时还支持自定义层解析、非最大抑制操作、获取各层的信息等。OpenCV加载模型的通用API为
    Net cv::dnn::readNet(
        const String & 	model,
        const String & 	config = "",
        const String & 	framework = "" 
    )
    model二进制训练好的网络权重文件，可能来自支持的网络框架，扩展名为如下：
    *.caffemodel (Caffe, http://caffe.berkeleyvision.org/)
    *.pb (TensorFlow, https://www.tensorflow.org/)
    *.t7 | *.net (Torch, http://torch.ch/)
    *.weights (Darknet, https://pjreddie.com/darknet/)
    *.bin (DLDT, https://software.intel.com/openvino-toolkit)

    config针对模型二进制的描述文件，不同的框架配置文件有不同扩展名
    *.prototxt (Caffe, http://caffe.berkeleyvision.org/)
    *.pbtxt (TensorFlow, https://www.tensorflow.org/)
    *.cfg (Darknet, https://pjreddie.com/darknet/)
    *.xml (DLDT, https://software.intel.com/openvino-toolkit)

    framework显示声明参数，说明模型使用哪个框架训练出来的

    拓展资料：
        OpenCV deep learning module samples：https://github.com/opencv/opencv/tree/master/samples/dnn
        Deep Neural Networks (dnn module)：https://docs.opencv.org/4.5.3/d2/d58/tutorial_table_of_content_dnn.html
        Deep Neural Network module：https://docs.opencv.org/4.5.3/d6/d0f/group__dnn.html
        cv::dnn::Net Class Reference：https://docs.opencv.org/4.5.3/db/d30/classcv_1_1dnn_1_1Net.html
        cv::dnn::Layer Class Reference：https://docs.opencv.org/4.5.3/d3/d6c/classcv_1_1dnn_1_1Layer.html
'''

import cv2 as cv

caffe_model_path = '../data/models/googlenet/bvlc_googlenet.caffemodel'
prototxt_path = '../data/models/googlenet/bvlc_googlenet.prototxt'

# 加载模型
# net = cv.dnn.readNetFromCaffe(prototxt_path, caffe_model_path)
net = cv.dnn.readNet(caffe_model_path, prototxt_path)

# 获取模型各层的名称
layer_names = net.getLayerNames()
for name in layer_names:
    # 通过名称获取层的id
    id = net.getLayerId(name)
    # 通过层的id获取layer对象
    layer = net.getLayer(id)
    print(f"layer id: {id}, name: {layer.name}, type: {layer.type}")
# 获取网络计算量
print("flops [input size (1, 3, 224, 224)]: ", net.getFLOPS((1, 3, 224, 224)))
