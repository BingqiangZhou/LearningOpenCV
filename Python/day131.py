'''
Author       : Bingqiang Zhou
Date         : 2021-09-03 17:49:29
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-03 18:15:37
Description  : OpenCV DNN 支持YOLOv3-tiny版本实时对象检测
    YOLOv3的模型在CPU上无法做到实时运行，而YOLO作者提供了个YOLOv3版本的精简版对象检测模型，
    大小只有30MB左右，但是模型可以在CPU上做到实时运行，这个模型就是YOLOv3-tiny模型，其下载地址如下：
    YOLO: Real-Time Object Detection：https://pjreddie.com/darknet/yolo/

    相比YOLOv3，YOLOv3-tiny只有两个输出层，而且权重参数层与参数文件大小都大大的下降，可以在嵌入式设备与前端实时运行。
'''

import cv2 as cv
import numpy as np

model_path = '../data/models/yolov3/yolov3-tiny.weights'
cfg_path = '../data/models/yolov3/yolov3-tiny.cfg'

# 加载模型并设置合适的计算后台和计算设备
net = cv.dnn.readNetFromDarknet(cfg_path, model_path)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

out_names = net.getUnconnectedOutLayersNames()

classes_path = '../data/models/yolov3/object_detection_classes_yolov3.txt'

# 对于分类类别
with open(classes_path, 'r') as f:
    classes = [ s.strip() for s in f.readlines()]

# 开启摄像头
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read() # 读取视频帧
    if ret is False:
        break

    h, w = frame.shape[:2]
    blob = cv.dnn.blobFromImage(frame, 1.0/255.0, (320, 320), (), swapRB=False, crop=False)

    # 预测
    net.setInput(blob)
    outs = net.forward(out_names)
    
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
        cv.rectangle(frame, boxes[i], (0, 0, 255), 2)
        out_str = f"object: {classes[i]}, score: {confidences[i]}"
        cv.putText(frame, out_str, (boxes[i][0]-5, boxes[i][1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, 8)

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

