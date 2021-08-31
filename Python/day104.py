'''
Author       : Bingqiang Zhou
Date         : 2021-08-31 18:07:24
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-31 19:10:56
Description  : SVM线性分类器
    对于得到的结构化HOG特征数据，我们就可以通过初始化SVM进行回归分类训练，这里采用的训练器是SVM线性分类器，
    SVM还有另外一个分类器就是对于线性不可分数据的径向分类器。
    OpenCV中使用径向分类器SVM有时候会训练很长时间，而且结果很糟糕，甚至会报一些莫名其妙的错误，感觉不是特别好。
    所以推荐大家真对线性不可分的问题可以选择神经网络ANN模块。

    在训练之前，首先简单的认识一下SVM，我们这边是通过二分类来完成，是很典型的线性可分离的SVM。
    
    对线性可分的选择用SVM，通过很少的样本学习就会取得很好的效果。OpenCV中SVM训练的API如下：
    virtual bool cv::ml::StatModel::train(
        InputArray 	samples,
        int layout,
        InputArray 	responses 
    )
    Sample表示训练样本数据/HOG特征数据
    Layout 有两种组织方式ROW_SAMPLE与COL_SAMPLE
    Responses 每个输入样本的标签

    对于训练好的数据我们可以通过save方法进行保存，只要提供一个保存路径即可。

    拓展资料：
        官方教程：
            Understanding SVM：https://docs.opencv.org/4.5.3/d4/db1/tutorial_py_svm_basics.html
            OCR of Hand-written Data using SVM：https://docs.opencv.org/4.5.3/dd/d3b/tutorial_py_svm_opencv.html
        官方文档：
            cv::ml::StatModel Class Reference：https://docs.opencv.org/master/db/d7d/classcv_1_1ml_1_1StatModel.html
            cv::ml::SVM Class Reference：https://docs.opencv.org/4.5.3/d1/d2d/classcv_1_1ml_1_1SVM.html
'''

import os
import time
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
        
    return np.array(train_datas, dtype=np.float32), np.array(labels, dtype=np.int32).reshape(-1, 1)
# 训练SVM分类器
def train_svm(train_datas, labels, model_save_path=None):
    svm = cv.ml.SVM_create()
    svm.setKernel(cv.ml.SVM_LINEAR)
    svm.setType(cv.ml.SVM_C_SVC)
    svm.setC(2.67)
    svm.setGamma(5.383)
    svm.train(samples=train_datas, layout=cv.ml.ROW_SAMPLE, responses=labels)
    if model_save_path is None:
        svm.save('svm.xml')
    else:
        svm.save(model_save_path)

# 数据集下载地址：https://github.com/gloomyfish1998/opencv_tutorial/blob/master/data/dataset/elec_watch.zip
positive_dir = "../data/datasets/elec_watch/positive"
negative_dir = "../data/datasets/elec_watch/negative"
train_datas, labels = generate_dataset(positive_dir, negative_dir, label_ids=[1, -1])
print(f"train_datas: {train_datas.shape}, labels: {labels.shape}")
start_time = time.time()
train_svm(train_datas, labels, model_save_path="../data/models/elec_watch_svm.xml")
end_time = time.time()
print(f"svm trained, use time: {end_time-start_time}s")