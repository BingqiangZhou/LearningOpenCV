'''
Author       : Bingqiang Zhou
Date         : 2021-08-30 10:01:48
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-30 10:31:55
Description  : 对象检测-LBP特征介绍
    局部二值模式(Local Binary Pattern)主要用来实现2D图像纹理分析。
    其基本思想是用每个像素跟它周围的像素相比较得到局部图像结构，
    假设中心像素值大于相邻像素值则则相邻像素点赋值为1，否则赋值为0，最终对每个像素点都会得到一个二进制八位的表示，
    比如11100111。假设3x3的窗口大小，这样对每个像素点来说组合得到的像素值的空间为[0~2^8]。
    这种结果称为图像的局部二值模式或者简写为了LBP。
    拓展资料：
        LBP特征原理及代码实现：https://blog.csdn.net/quincuntial/article/details/50541815
        详解LBP特征与应用(人脸识别)：https://mp.weixin.qq.com/s/Rm5HuERAA1j_7lE2HcyoqA
'''

import os
import cv2 as cv

# 初始化lbpcascades检测器
# xml file from: https://github.com/opencv/opencv/tree/master/data/lbpcascades
xml_file = os.path.join("../data/cv/lbpcascades", 'lbpcascade_frontalface_improved.xml')
detector = cv.CascadeClassifier(xml_file)

# 开启摄像头
cap = cv.VideoCapture(0)
while True:
    success, frame = cap.read()
    if not success:
        break

    # 均衡化图像直方图（增加一下对比度）
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.equalizeHist(gray)

    # 人脸检测
    faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, flags=0, minSize=(30, 30), maxSize=(400, 400))
    
    # 可视化检测到的人脸
    for face_rect in faces:
        cv.rectangle(frame, face_rect, (0, 255, 0), 2)
    cv.imshow("CascadeClassifier", frame)
    key = cv.waitKey(50)
    if key == 27:
        break

cv.destroyAllWindows()
cap.release()
