'''
Author       : Bingqiang Zhou
Date         : 2021-09-03 17:06:27
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-03 18:13:01
Description  : OpenCV DNN 支持YOLO对象检测网络运行
    OpenCV DNN模块支持YOLO对象检测网络，最新的OpenCV4.0支持YOLOv3版本的对象检测网络，
    YOLOv3版本同时还发布了移动端支持的网络模型YOLOv3-tiny版本，速度可以在CPU端实时运行的对象检测网络，
    OpenCV中通过对DarkNet框架集成支持实现YOLO网络加载与检测。
    因为YOLOv3对象检测网络是多个层的合并输出，所以在OpenCV中调用时候必须显示声明那些是输出层，
    这个对于对象检测网络，OpenCV提供了一个API来获取所有的输出层名称，该API为：
    std::vector<String> cv::dnn::Net::getUnconnectedOutLayersNames()const
    该函数返回所有非连接的输出层。

    调用时候，必须显式通过输入参数完成推断，相关API如下：
    void cv::dnn::Net::forward(
        OutputArrayOfArrays outputBlobs,
        const std::vector< String > & outBlobNames
    )
    outputBlobs是调用之后的输出
    outBlobNames是所有输出层的名称

    跟SSD/Faster-RCNN出来的结构不一样，YOLO的输出前四个为
    # [center_x, center_y, width, height]
    后面的是所有类别的得分，这个时候只要根据score大小就可以得到score最大的对应对象类别，解析检测结果。
    相关模型下载到YOLO作者的官方网站：
    YOLO: Real-Time Object Detection：https://pjreddie.com/darknet/yolo/

    拓展资料：
        对象检测网络中的NMS算法详解：https://mp.weixin.qq.com/s/yccBloK5pOVxDIFkmoY7xg
        OpenCV中使用YOLO对象检测：https://mp.weixin.qq.com/s/95hftpJfSDIMlMVOC7iq4g
'''

import cv2 as cv
import numpy as np

model_path = '../data/models/yolov3/yolov3.weights'
cfg_path = '../data/models/yolov3/yolov3.cfg'

classes_path = '../data/models/yolov3/object_detection_classes_yolov3.txt'

# 对于分类类别
with open(classes_path, 'r') as f:
    classes = [ s.strip() for s in f.readlines()]

# 加载模型并设置合适的计算后台和计算设备
net = cv.dnn.readNetFromDarknet(cfg_path, model_path)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# 读取图片
# img = cv.imread("../data/images/dog.jpg")
img = cv.imread("../data/images/objects.jpg")
h, w = img.shape[:2]
blob = cv.dnn.blobFromImage(img, 1.0/255.0, (320, 320), (), swapRB=False, crop=False)

# 预测
out_names = net.getUnconnectedOutLayersNames()
net.setInput(blob)
outs = net.forward(out_names)

# 绘制检测矩形
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        # 前4个是 [center_x, center_y, width, height]，后面81一个是对象类别的分数
        scores = detection[5:]
        classId = np.argmax(scores)
        confidence = scores[classId]
        if confidence > 0.5:
            center_x = int(detection[0] * w)
            center_y = int(detection[1] * h)
            width = int(detection[2] * w)
            height = int(detection[3] * h)
            left = int(center_x - width / 2)
            top = int(center_y - height / 2)
            class_ids.append(classId)
            confidences.append(float(confidence))
            boxes.append([left, top, width, height])

indices = cv.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)

for i in indices:
    i = i[0]
    cv.rectangle(img, boxes[i], (0, 0, 255), 2)
    out_str = f"object: {classes[i]}, score: {confidences[i]}"
    cv.putText(img, out_str, (boxes[i][0]-5, boxes[i][1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, 8)

# 获取推理时间、类别等信息
t, timings = net.getPerfProfile() # t为总时间，timings为每一层的时间
use_time = t / cv.getTickFrequency()
print(f"use time {use_time}s")

# 可视化
# cv.putText(img, out_str, (0, 20), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
cv.imshow("result", img)
cv.waitKey(0)
cv.destroyAllWindows()
