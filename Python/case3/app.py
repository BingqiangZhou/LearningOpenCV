'''
Author       : Bingqiang Zhou
Date         : 2021-09-10 00:24:29
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-10 10:23:36
Description  : 案例三 - DNN 人脸识别
    人脸识别基本流程：
        1. 使用人脸检测模型，实现对图像或者视频的人脸检测
        2. 对得到的人脸区域通过人脸识别模型提取特征向量
        3. 基于余弦相似度进行特征值比对，实现人脸识别
    参考：
        OpenCV4.0实现人脸识别 - https://mp.weixin.qq.com/s/tITsD0XAZq25PSPX2G5k0Q
        facenet网络 - https://github.com/davidsandberg/facenet
'''

import cv2 as cv
import numpy as np

# 人脸检测模型
face_detection_cfg = "./models/deploy.prototxt"
face_detection_model = "./models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
face_detection_net = cv.dnn.readNetFromCaffe(face_detection_cfg, face_detection_model)

# 人脸识别模型
face_recognition_model = "./models/openface.nn4.small2.v1.t7"
face_recognition_net = cv.dnn.readNetFromTorch(face_recognition_model)

# 对输入图像进行人脸检测并返回bbox，以及bbox向外扩张50个像素的人脸roi
def face_detect(image, expand=50):
    blob = cv.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0), False, False)
    face_detection_net.setInput(blob)
    out = face_detection_net.forward("detection_out") # (1, 1, 200, 7)
    # 7维分别为 [图像标号，对象的id，置信度，bbox的坐标比率（需要乘以原高宽大小）left, top, right, bottom]
    index = np.nonzero(out[0, 0, :, 2] > 0.5)

    h, w = image.shape[:2]
    faces_roi = []
    rects = []
    for i in index[0]:
        rect = out[0, 0, i, 3:]
        rect = (int(rect[0]*w), int(rect[1]*h), int(rect[2]*w), int(rect[3]*h))
        rects.append(rect)
        # 向四个方向扩充50个像素
        faces_roi.append(image[max(0, rect[1] - expand):min(h, rect[3] + expand),\
                                max(0, rect[0] - expand):min(w, rect[2] + expand)].copy())
        # cv.rectangle(image, (rect[0], rect[1]), (rect[2], rect[3]), (0, 0, 255), 2, 8)
        # cv.imshow("face", faces_roi[-1])
    if len(faces_roi) > 0:
        cv.imwrite("bqz_1.png", faces_roi[-1])
    return faces_roi, rects

# 人脸识别，返回特征向量
def face_recognize_fv(face_image):
    blob = cv.dnn.blobFromImage(face_image, 1.0/255.0, (96, 96), (0, 0, 0), True, False)
    face_recognition_net.setInput(blob)
    fv = face_recognition_net.forward()
    return fv.flatten() # (128, )

# 计算余弦相似度
def cos_similar(v1, v2):
    return np.sum(v1 * v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# 人脸识别，与模版资料比较，输出最相似的人脸的人名
def face_recognize(face_image, face_fv_templates, threshold_v=0.8):
    fv = face_recognize_fv(face_image)
    score_list = []
    for k, v in face_fv_templates.items():
        score = cos_similar(fv, v)
        score_list.append(score)
    index = np.argmax(score_list)
    # print(score_list, index)
    name = None
    if score_list[index] > threshold_v:
        name = list(face_fv_templates.keys())[index]
        # print("This is ", name)
    return name

# 人脸模版对应人名以及图像路径
face_templates = {
    "balvin": "./images/balvin_1.png",
    "zhigang": "./images/zhigang_1.png",
}

# 构建模版资料库
face_fv_templates = {}
for k, v in face_templates.items():
    img = cv.imread(v)
    fv = face_recognize_fv(img)
    # print(fv.shape)
    face_fv_templates.update({k: fv})
# print(face_fv_templates)

# 对图片进行识别，阈值设置为0.8
face_img = cv.imread("./images/balvin_2.png")
# face_img = cv.imread("./images/zhigang_2.png")
name = face_recognize(face_img, face_fv_templates)
print("This is ", name)

# 对视频进行识别
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # 人脸检测
    faces, rects = face_detect(frame)

    # 识别并可视化结果
    for i, face_roi in enumerate(faces):
        name = face_recognize(face_roi, face_fv_templates)
        if name is not None:
            out_str = f'This is {name}'
        else:
            out_str = 'not found'
        cv.rectangle(frame, (rects[i][0], rects[i][1]), (rects[i][2], rects[i][3]), (0, 0, 255), 2, 8)
        cv.putText(frame, out_str, (rects[i][0], rects[i][1]-20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
    
    cv.imshow("frame", frame)

    k = cv.waitKey(50)
    if k == 27:
        break

cv.destroyAllWindows()

