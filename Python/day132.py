'''
Author       : Bingqiang Zhou
Date         : 2021-09-03 21:09:39
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-03 21:18:20
Description  : OpenCV DNN单张与多张图像的推断
    OpenCV DNN中支持单张图像推断，同时还支持分批次方式的图像推断，
    对应的两个相关API分别为blobFromImage与blobFromImages，它们的返回对象都是一个四维的Mat对象-按照顺序分别为NCHW 
    其组织方式详解如下：
    N表示多张图像
    C表示接受输入图像的通道数目
    H表示接受输入图像的高度
    W表示接受输入图像的宽度
    Mat cv::dnn::blobFromImage(
        InputArray 	image,
        double 	scalefactor = 1.0,
        const Size & 	size = Size(),
        const Scalar & 	mean = Scalar(),
        bool 	swapRB = false,
        bool 	crop = false,
        int 	ddepth = CV_32F
    )

    Mat cv::dnn::blobFromImages(
        InputArrayOfArrays 	images,
        double 	scalefactor = 1.0,
        Size 	size = Size(),
        const Scalar & 	mean = Scalar(),
        bool 	swapRB = false,
        bool 	crop = false,
        int 	ddepth = CV_32F 
    )
    参数解释
    Images表示多张图像,image表示单张图像
    Scalefactor表示放缩
    Size表示图像大小
    Mean表示均值
    swapRB是否交换通道
    crop是否剪切
    ddepth 输出的类型，默认是浮点数格式
'''

import cv2 as cv
import numpy as np

caffe_model_path = '../data/models/googlenet/bvlc_googlenet.caffemodel'
prototxt_path = '../data/models/googlenet/bvlc_googlenet.prototxt'
classes_path = '../data/models/googlenet/classification_classes_ILSVRC2012.txt'

# 对于分类类别
with open(classes_path, 'r') as f:
    classes = [ s.strip() for s in f.readlines()]

# 加载模型并设置合适的计算后台和计算设备
net = cv.dnn.readNetFromCaffe(prototxt_path, caffe_model_path)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# 读取图片
img1 = cv.imread("../data/images/flower.png")
img2 = cv.imread("../data/images/test1.png")
image_list = [img1, img2]
blob = cv.dnn.blobFromImages(image_list, 1.0, (224, 224), (), swapRB=False, crop=False)

# 预测
net.setInput(blob)
outs = net.forward() # (n, 1000)

# 获取推理时间、类别等信息
t, timings = net.getPerfProfile()
use_time = t / cv.getTickFrequency()
print(f" use time {use_time}s")

for i in range(outs.shape[0]):
    index = np.argmax(outs[i])
    out_str = f'class: {classes[index]}, confidence: {outs[i][index]}'
    print(out_str)
    # 可视化
    cv.putText(image_list[i], out_str, (0, 20), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
    cv.imshow(f"result {i}", image_list[i])
cv.waitKey(0)
cv.destroyAllWindows()