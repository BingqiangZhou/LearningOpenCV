'''
Author       : Bingqiang Zhou
Date         : 2021-08-31 16:32:03
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-31 18:08:02
Description  : HOG特征描述子 – 使用描述子特征生成样本数据
    对于HOG特征，我们可以通过预先训练的特征数据，进行多尺度的对象检测，OpenCV中基于HOG的行人检测是一个典型案例，
    同时我们还可以实现自定义对象的检测，这种自定义对象检测，可以分为两个部分，
    第一部分：通过提取样本的HOG描述子，生成样本的特征数据，
    第二部分通过SVM进行分类学习与训练，保存为模型。
    这样我们以后就可以通过模型来实现自定义对象检测啦。
    今天我们分享第二部分，使用HOG描述子特征数据生成数据集，进行SVM分类训练，实现对象分类识别。
    
    这里我已一个很常见的应用，电表检测为例，这类问题早期主要通过特征匹配实现，
    但是这个方法比较容易受到各种因素干扰，不是很好，通过提取HOG特征、进行SVM特征分类、然后开窗检测，是一个很好的解决方法。

    在OpenCV中训练SVM模型，其数据格式常见的是“行模式”就是一行（多列向量）是一个样本，对应一个整数标签(label)。
    这里采用默认的窗口大小为64x128 提取HOG特征向量，得到的每个样本的向量数目等于7x15x36=3780，
    有多少个样本就有多少行， 对于的标签是每一行对应自己的标签，有多少个训练样本，标签就有多少行！
'''

import os
import cv2 as cv
import numpy as np

def get_hog_descriptor(image, show=True):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    h, w = gray.shape
    # 根据是高还是宽对HOG窗口大小64x128的比例更高，决定后续对图像做resize以及padding，确保高或者宽的像素占满
    flag = np.argmax((h/128, w/64)) 
    bg = np.full((128, 64), 127, dtype=np.uint8) # padding的为127
    if flag == 1:
        rate = 64 / w
        h_resize = int(h * rate)
        gray_resized = cv.resize(gray, (64, h_resize))
        dh = (128 - h_resize) // 2
        bg[dh:h_resize+dh, :] = gray_resized

    else: # flag == 0
        rate = 128 / h
        w_resize = int(64 * rate)
        gray_resized = cv.resize(gray, (w_resize, 128))
        dw = (64 - w_resize) // 2
        bg[:, dw:w_resize+dw] = gray_resized
    
    if show:
        print(gray_resized.shape, bg.shape)
        cv.imshow("gray", gray_resized)
        cv.imshow("bg", bg)
        cv.waitKey(0)

    # 计算hog特征描述子
    hog = cv.HOGDescriptor()
    hog_desc = hog.compute(bg, winStride=(8, 8), padding=(0, 0))
    return hog_desc # (3780, 1)

def generate_dataset(*dirs, label_ids=[1, -1]):
    # 传入文件夹路径，默认顺序为正样本文件夹，负样本文件夹
    train_datas = []
    labels = []
    for i, cur_dir in enumerate(dirs):
        for img_name in os.listdir(cur_dir):
            img_path = os.path.join(cur_dir, img_name)
            img = cv.imread(img_path)
            feature_vector = get_hog_descriptor(img, show=False) #(3780, 1)
            train_datas.append(feature_vector.flatten().tolist())
            labels.append(label_ids[i])
        
    return np.array(train_datas, dtype=np.float32), np.array(labels, dtype=np.float32).reshape(-1, 1)

# 数据集下载地址：https://github.com/gloomyfish1998/opencv_tutorial/blob/master/data/dataset/elec_watch.zip
positive_dir = "../data/datasets/elec_watch/positive"
negative_dir = "../data/datasets/elec_watch/negative"
train_datas, labels = generate_dataset(positive_dir, negative_dir, label_ids=[1, -1])
print(train_datas.shape, labels.shape)

