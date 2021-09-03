'''
Author       : Bingqiang Zhou
Date         : 2021-09-03 23:48:14
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-04 00:16:04
Description  : OpenCV DNN ENet实现图像分割
    OpenCV DNN支持ENet网络模型的图像分割，这里采用的预先训练的ENet网络模型下载地址如下：
    https://github.com/e-lab/ENet-training    

    该模型是torch模型，加载的API为：
    Net cv::dnn::readNetFromTorch(
        const String & 	model,
        bool 	isBinary = true 
    )
    model参数表示二进制的模型权重文件
    isBinary 默认为true

    跑ENet网络的时候，OpenCV4.0.x与DLIE一起编译之后，当使用
    DNN_BACKEND_INFERENCE_ENGINE，作为推断后台的时候，会得到上采样最大池化错误
    切换为DNN_BACKEND_OPENCV 则torch模型正常加载！
'''

import cv2 as cv
import numpy as np

model_path = '../data/models/enet/model-cityscapes.net'

# 加载模型
net = cv.dnn.readNetFromTorch(model_path)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# 读取图片
img = cv.imread("../data/images/city.png")
blob = cv.dnn.blobFromImage(img, 1.0/255.0, (512, 512), (), swapRB=False, crop=False)

# 预测
net.setInput(blob)
outs = net.forward() # (n, 1000)
print(outs.shape)

# 获取推理时间、类别等信息
t, timings = net.getPerfProfile()
use_time = t / cv.getTickFrequency()
print(f" use time {use_time}s")

index = np.argmax(outs, axis=1)
color_map = np.random.randint(0, 255, (20, 3), dtype=np.uint8)
new_img = color_map[index[0], :]
new_img = cv.resize(new_img, img.shape[:2][::-1])

mask = cv.cvtColor(index[0].astype(np.uint8), cv.COLOR_GRAY2BGR)
cv.normalize(mask, mask, 0, 255, cv.NORM_MINMAX)
cmask = cv.applyColorMap(mask, cv.COLORMAP_JET)
cmask = cv.resize(cmask, img.shape[:2][::-1])
dst = cv.addWeighted(img, 0.7, cmask, 0.3, 0)

# 可视化
cv.imshow(f"img", img)
cv.imshow(f"result", new_img)
cv.imshow(f"dst", dst)
cv.waitKey(0)
cv.destroyAllWindows()
