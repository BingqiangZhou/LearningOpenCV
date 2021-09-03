'''
Author       : Bingqiang Zhou
Date         : 2021-09-04 01:25:53
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-04 02:12:33
Description  : OpenCV DNN 实现性别与年龄预测
    学会在OpenCV DNN中如何调用多个模型，相互配合使用！
    Gender Net and Age Net
    上述两个模型一个是预测性别的，一个是预测年龄的。

    性别预测返回的是一个二分类结果
    Male
    Female

    年龄预测返回的是8个年龄的阶段！
    '(0-2)', 
    '(4-6)', 
    '(8-12)', 
    '(15-20)', 
    '(25-32)', 
    '(38-43)', 
    '(48-53)', 
    '(60-100)'

    实现步骤
    完整的实现步骤需要如下几步：
    预先加载三个网络模型
    打开摄像头视频流/加载图像
    对每一帧进行人脸检测
    - 对检测到的人脸进行性别与年龄预测
    - 解析预测结果
    - 显示结果
'''

import cv2 as cv
import numpy as np

face_model_path = '../data/models/face_detector/opencv_face_detector_uint8.pb'
face_protxt = '../data/models/face_detector/opencv_face_detector.pbtxt'
gender_model_path = '../data/models/age_gender_models/gender_net.caffemodel'
gender_protxt = '../data/models/age_gender_models/gender_deploy.prototxt'
age_model_path = '../data/models/age_gender_models/age_net.caffemodel'
age_protxt = '../data/models/age_gender_models/age_deploy.prototxt'



# 加载模型
face_net = cv.dnn.readNetFromTensorflow(face_model_path, face_protxt)
gender_net = cv.dnn.readNetFromCaffe(gender_protxt, gender_model_path)
age_net = cv.dnn.readNetFromCaffe(age_protxt, age_model_path)

age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
gender_list = ['Male', 'Female']

# 开启摄像头
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read() # 读取视频帧
    if ret is False:
        break
    
    h, w = frame.shape[:2]

    blob = cv.dnn.blobFromImage(frame, 1.0, (300, 300), (), swapRB=False, crop=False)
    face_net.setInput(blob)
    out = face_net.forward() # (1, 1, 200, 7)
    index = np.nonzero(out[0, 0, :, 2] > 0.5)
    if len(index[0]) > 0:
        face = (out[0, 0, index[0], 3:] * [w, h, w, h]).astype(np.int)
        cv.rectangle(frame, (face[0][0], face[0][1]), (face[0][2], face[0][3]), (0, 0, 255), 2, 8)
        face_roi = frame[face[0][1]:face[0][3], face[0][0]:face[0][2]]
        
        blob = cv.dnn.blobFromImage(face_roi, 1.0, (227, 227), (), swapRB=False, crop=False)

        # 预测性别
        gender_net.setInput(blob)
        out = gender_net.forward()
        gender_index = np.argmax(out[0]) #  0: Male, 1:Female

        # 预测年龄
        age_net.setInput(blob)
        out = age_net.forward()
        age_index = np.argmax(out[0]) 

        out_str = f"gender: {gender_list[gender_index]}, age: {age_list[age_index]}"
        cv.putText(frame, out_str, (face[0][0], face[0][1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, 8)
        
        # 获取推理时间
        use_time = 0
        t, timings = face_net.getPerfProfile() # t为总时间，timings为每一层的时间
        use_time += t / cv.getTickFrequency()
        t, timings = age_net.getPerfProfile() # t为总时间，timings为每一层的时间
        use_time += t / cv.getTickFrequency()
        t, timings = gender_net.getPerfProfile() # t为总时间，timings为每一层的时间
        use_time += t / cv.getTickFrequency()
        fps = 1 / use_time
        cv.putText(frame, f'fps: {fps}', (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, 8)
        # print(f"use time {use_time}s, fps {fps}")

    # # 可视化
    cv.imshow("result", frame)
    key = cv.waitKey(50)
    if key == 27:
        break

cv.destroyAllWindows()

