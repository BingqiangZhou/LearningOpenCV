'''
Author       : Bingqiang Zhou
Date         : 2021-09-03 15:48:49
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-03 17:01:36
Description  : OpenCV DNN 调用openpose模型实现姿态评估
    OpenCV DNN模块中使用openopse的深度学习模型,实现人体单人姿态评估, 首先需要下载人体姿态评估的预训练模型。
    基于COCO数据集训练的模型下载地址如下：
    http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/coco/pose_iter_440000.caffemodel
    https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/openpose_pose_coco.prototxt

    基于MPI数据集训练的模型下载地址如下：
    http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/mpi/pose_iter_160000.caffemodel
    https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/openpose_pose_mpi_faster_4_stages.prototxt

    手势姿态模型
    http://posefs1.perception.cs.cmu.edu/OpenPose/models/hand/pose_iter_102000.caffemodel
    https://raw.githubusercontent.com/CMU-Perceptual-Computing-Lab/openpose/master/models/hand/pose_deploy.prototxt

    其中COCO模型会生成18个点，MPI模型生成14个点，手势姿态模型生成20个点，根据这些点可以绘制出人体的关键节点或者手的关键节点。OpenCV DNN支持的姿态评估都是基于预训练的Caffe模型，而且模型没有经过专门的优化处理，速度特别的慢，在CPU上基本是秒级别才可以出结果，离实时运行差好远，但是对一些静态的手势分析还是有一定的帮助与作用。
    代码实现可以分为如下几个步骤
    1.	加载网络
    2.	获取heatmap数据，根据heatmap寻找最大score与位置信息
    3.	根据位置信息，绘制连接直线
'''

import cv2 as cv
import numpy as np

BODY_PARTS_COCO = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS_COCO = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]
BODY_PARTS_MPI = { "Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
                "Background": 15 }
POSE_PAIRS_MPI = [ ["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
                ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
                ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
                ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"] ]

def predict(net, img):
    sh, sw = img.shape[:2]
    # 读取图片
    blob = cv.dnn.blobFromImage(img, 1/255.0, (300, 300), (), swapRB=False, crop=False)

    # 预测
    net.setInput(blob)
    out = net.forward()
    h, w = out.shape[2:]
    print(out.shape)
    out_loc = []
    for i in range(len(out[0])):
        minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(out[0][i])
        print(minVal, maxVal, minLoc, maxLoc)
        maxLoc = (int(maxLoc[0] * sw / w), int(maxLoc[1] * sh / h)) # 与原图像和heatmap大小比值相乘
        # 可视化
        if maxVal > 0.5:
            out_loc.append(maxLoc)
            cv.circle(img, maxLoc, 5, (0, 0, 255), 2, 8)
        else:
            out_loc.append((-1, -1))
    # 获取推理时间、类别等信息
    t, timings = net.getPerfProfile() # t为总时间，timings为每一层的时间
    use_time = t / cv.getTickFrequency()
    print(f"use time {use_time}s")

    return out_loc, t


body_pose_coco_caffe_model_path = '../data/models/openpose_pose/pose_iter_440000.caffemodel'
body_pose_coco_prototxt_path = '../data/models/openpose_pose/openpose_pose_coco.prototxt'

body_pose_mpi_caffe_model_path = '../data/models/openpose_pose/pose_iter_160000.caffemodel'
body_pose_mpi_prototxt_path = '../data/models/openpose_pose/openpose_pose_mpi_faster_4_stages.prototxt'

hand_pose_caffe_model_path = '../data/models/openpose_pose/pose_iter_102000.caffemodel'
hand_pose_prototxt_path = '../data/models/openpose_pose/pose_deploy.prototxt'

img_hand = cv.imread("../data/images/hand.jpg")
img_body = cv.imread("../data/images/stand.jpg")

# 加载模型
body_pose_coco_net = cv.dnn.readNetFromCaffe(body_pose_coco_prototxt_path, body_pose_coco_caffe_model_path)
img_body_coco = img_body.copy()
out, t = predict(body_pose_coco_net, img_body_coco)

body_pose_mpi_net = cv.dnn.readNetFromCaffe(body_pose_mpi_prototxt_path, body_pose_mpi_caffe_model_path)
img_body_mpi = img_body.copy()
out, t = predict(body_pose_mpi_net, img_body_mpi)

hand_pose_net = cv.dnn.readNetFromCaffe(hand_pose_prototxt_path, hand_pose_caffe_model_path)
out, t = predict(hand_pose_net, img_hand)

# 可视化
cv.imshow("img_body_coco", img_body_coco)
cv.imshow("img_body_mpi", img_body_mpi)
cv.imshow("img_hand", img_hand)
cv.waitKey(0)
cv.destroyAllWindows()
