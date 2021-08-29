'''
Author       : Bingqiang Zhou
Date         : 2021-08-29 23:00:18
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-30 00:13:16
Description  : 对象检测 – HAAR级联检测器使用
    HAAR级联检测器，OpenCV中的HAAR级联检测器支持人脸检测、微笑、眼睛与嘴巴检测等，
    通过加载这些预先训练的HAAR模型数据可以实现相关的对象检测，
    void cv::CascadeClassifier::detectMultiScale(
        InputArray 	image,
        std::vector&lt; Rect &gt; & objects,
        double scaleFactor = 1.1,
        int minNeighbors = 3,
        int flags = 0,
        Size minSize = Size(),
        Size maxSize = Size() 
    )
    各个参数解释如下:
    Image:输入图像
    Objects 人脸框
    ScaleFactor 放缩比率
    minNeighbors 表示最低相邻矩形框
    flags 标志项OpenCV3.x以后不用啦，
    minSize 可以检测的最小人脸
    maxSize 可以检测的最大人脸
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
print(cv.data.haarcascades)
xml_file = os.path.join(cv.data.haarcascades, 'haarcascade_frontalface_alt2.xml')
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
