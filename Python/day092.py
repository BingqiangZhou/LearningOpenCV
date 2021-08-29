'''
Author       : Bingqiang Zhou
Date         : 2021-08-30 00:11:51
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-30 00:29:48
Description  : 对象检测-HAAR特征介绍
    HAAR小波基函数，因为其满足对称性，对人脸这种生物对称性良好的对象特别适合用来做检测器，
    常见的Haar特征分为三类：
        边缘特征、
        线性特征、
        中心特征和对角线特征，
    不同特征可以进行多种组合，生成更加复杂的级联特征，特征模板内有白色和黑色两种矩形，
    并定义该模板的特征值为白色矩形像素和减去黑色矩形像素和，Haar特征值反映了图像的对比度与梯度变化。
    OpenCV中HAAR特征计算是积分图技术，这个我们在前面也分享过啦，所以可以非常快速高效的开窗检测，
    HAAR级联检测器具备有如下特性：
        - 高类间变异性
        - 低类内变异性
        - 局部强度差
        - 不同尺度
        - 计算效率高
    拓展资料：
        haar+adaboost结合讲解（偏重实际）：https://blog.csdn.net/playezio/article/details/80471000
        人脸检测之Haar分类器：https://www.cnblogs.com/zyly/p/9410563.html
'''

# 正面人脸：haarcascade_frontalface_default.xml、haarcascade_frontalface_alt_tree.xml、haarcascade_frontalface_alt.xml、haarcascade_frontalface_alt2.xml 
# 侧面人脸：haarcascade_profileface.xml
# 猫正脸：haarcascade_frontalcatface.xml、haarcascade_frontalcatface_extended.xml
# 车牌：haarcascade_licence_plate_rus_16stages.xml、haarcascade_russian_plate_number.xml
# 上身：haarcascade_upperbody.xml
# 下身：haarcascade_lowerbody.xml
# 人眼：haarcascade_eye.xml
# 左眼：haarcascade_lefteye_2splits.xml
# 右眼：haarcascade_righteye_2splits.xml
# 微笑：haarcascade_smile.xml
# 戴眼镜的眼睛：haarcascade_eye_tree_eyeglasses.xml 

import os
import cv2 as cv

# 初始化haarcascades检测器
# print(cv.data.haarcascades, os.listdir(cv.data.haarcascades))
face_detector = cv.CascadeClassifier(os.path.join(cv.data.haarcascades, 'haarcascade_frontalface_alt2.xml'))
smile_detector = cv.CascadeClassifier(os.path.join(cv.data.haarcascades, 'haarcascade_smile.xml'))

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
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, flags=0, minSize=(30, 30), maxSize=(400, 400))
    
    # 可视化检测到的人脸
    for face_rect in faces:
        cv.rectangle(frame, face_rect, (0, 255, 0), 2)
        x, y, w, h = face_rect
        if w > 0 and h > 0:
            face_roi = gray[y:y+h, x:x+w]
            smiles = face_detector.detectMultiScale(face_roi, scaleFactor=1.7, minNeighbors=3, flags=0, minSize=(15, 15), maxSize=(200, 200))
            for smile_rect in smiles:
                cv.rectangle(frame, (smile_rect[0]+x, smile_rect[1]+y, smile_rect[2], smile_rect[3]), (0, 0, 255), 2)
    cv.imshow("CascadeClassifier", frame)
    key = cv.waitKey(50)
    if key == 27:
        break

cv.destroyAllWindows()
cap.release()
