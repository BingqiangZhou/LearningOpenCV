'''
Author       : Bingqiang Zhou
Date         : 2021-09-04 00:25:52
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-04 00:47:01
Description  : OpenCV DNN 实时快速的图像风格迁移
    OpenCV DNN模块现在还支持图像风格迁移网络模型的加载与使用，
    支持的模型是基于李飞飞等人在论文《Perceptual Losses for Real-Time Style Transfer and Super-Resolution》
    中提到的快速图像风格迁移网络，基于感知损失来提取特征，生成图像特征与高分辨率图像。
    整个网络模型是基于DCGAN + 5个残差层构成，是一个典型的全卷积网络，关于DCGAN可以看这里有详细介绍与代码实现：
    https://mp.weixin.qq.com/s/8gSTociiFsHsDrxo-zrkgg

    模型下载地址
    https://github.com/jcjohnson/fast-neural-style

    这个网络可以支持任意尺寸的图像输入，作者提供了很多种预训练的风格迁移模型提供使用，我下载了下面的预训练模型。：
    composition_vii.t7
    starry_night.t7
    la_muse.t7
    the_wave.t7
    mosaic.t7
    the_scream.t7
    feathers.t7
    candy.t7
    udnie.t7
    这些模型都是torch框架支持的二进制权重文件，加载模型之后，就可以调用forward得到结果，通过对输出结果反向加上均值，
    rescale到0~255的RGB色彩空间，即可显示
'''

import os
import cv2 as cv
import numpy as np

base_dir = "../data/models/fast_neural_style"
styles = ["composition_vii.t7", "starry_night.t7", "la_muse.t7", "the_wave.t7",
          "mosaic.t7", "the_scream.t7", "feathers.t7", "candy.t7", "udnie.t7"]

# 加载模型
nets = []
for style in styles:
    net = cv.dnn.readNetFromTorch(os.path.join(base_dir, style))
    nets.append(net)

h, w = 224, 224

# 开启摄像头
cap = cv.VideoCapture(0)
result = np.zeros((h*3, w*3, 3))
while True:
    ret, frame = cap.read() # 读取视频帧
    if ret is False:
        break
    
    blob = cv.dnn.blobFromImage(frame, 1.0, (w, h), (), swapRB=False, crop=False)

    # 预测
    use_time = 0
    for i, net in enumerate(nets):
        row = i // 3
        col = i % 3
        net.setInput(blob)
        out = net.forward()
        out = out[0].transpose(1, 2, 0)
        result[row*h:row*h+h, col*w:col*w+w] = out
        # 获取推理时间
        t, timings = net.getPerfProfile() # t为总时间，timings为每一层的时间
        use_time += t / cv.getTickFrequency()
    fps = 1 / use_time
    cv.putText(result, f'fps: {fps}', (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, 8)
    # print(f"use time {use_time}s, fps {fps}")

    # 可视化
    cv.imshow("result", result)
    key = cv.waitKey(50)
    if key == 27:
        break

cv.destroyAllWindows()
