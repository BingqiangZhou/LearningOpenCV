'''
Author       : Bingqiang Zhou
Date         : 2021-08-31 15:39:17
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-31 16:28:46
Description  : HOG特征描述子 – 提取描述子
    对于HOG特征，我们可以通过预先训练的特征数据，进行多尺度的对象检测，OpenCV中基于HOG的行人检测是一个典型案例，
    同时我们还可以实现自定义对象的检测，这种自定义对象检测，可以分为两个部分，
    第一部分：通过提取样本的HOG描述子，生成样本的特征数据，
    第二部分通过SVM进行分类学习与训练，保存为模型。
    这样我们以后就可以通过模型来实现自定义对象检测啦。
    今天我们首先分享第一部分，提取HOG描述子。
    
    OpenCV中提取HOG描述子的API表示如下：
    virtual void cv::HOGDescriptor::compute(
        InputArray 	img,
        std::vector< float > & 	descriptors,
        Size 	winStride = Size(),
        Size 	padding = Size(),
        const std::vector< Point > & locations = std::vector< Point >() 
    )
    输入图像大小WxH=72x128
    默认的HOG描述子窗口大小为64x128，窗口移动的步长8x8
    对于每个窗口内部，每个Cell大小是8x8的，所以窗口可以划分为8x16的Cells大小
    对于每个Block区域来说，每次移动步长是一个Cell，8x16Cells可以得到总数7x15个Block
    每个Block都是4个Cell, 36个向量，所以对于输入图像得到：
    7x15x36x2 = 7560个特征描述子，这些描述子可以作为浮点数特征数据，对于需要输入的样本图像来说，需要首先执行以下预处理，
    把图像大小resize为跟窗口大小一致或者把窗口resize跟图像大小一致，这样有利于下一步处理。
'''

import cv2 as cv

img = cv.imread("../data/images/test1.png")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

hog = cv.HOGDescriptor()

gray_resized = cv.resize(gray, (72, 128))
hog_desc = hog.compute(gray_resized, winStride=(8, 8), padding=(0, 0))
print("image shape: ", gray_resized.shape)      # (128, 72) hxw
print("HOGDescriptor shape: ", hog_desc.shape)  # (7560, 1)
## 输入图像大小hxw:（72x128），默认的HOG描述子窗口大小为（64x128），窗口移动的步长（8x8），窗口只能向下滑动一次，即可以检测2次
## 对于HOG描述子窗口大小为（64x128），可划分为（8x16）个（8x8）的cells，而4个cells为一个block，即一个滑动窗口（16x16），
## 在（16x16）的block在HOG描述子窗口（64x128）上的以（8x8）的步长滑动，得到（(64-16)/8+1 x (128-16)/8+1）=（7x15）个block
## 而每个block有4个cell，每个cell的特征为bins为9的直方图，因此，一个block对于的特征大小为（36x1）
## 整个HOG描述子窗口的特征大小为（36x1）x（7x15）=（3780x1）
## 整张输入图像的特征大小为（3780x1）x 2 =（7560x1）

hog_desc = hog.compute(gray, winStride=(8, 8), padding=(0, 0))
print("image shape: ", gray.shape)              # (696, 579) hxw
print("HOGDescriptor shape: ", hog_desc.shape)  # (17690400, 1)
## （(696-128)/8+1 x (579-64)/8+1）*（3780x1）=（72x65）*（3780x1）= （17690400x1）


# 可视化
# cv.imshow("result", img)
# cv.waitKey(0)
# cv.destroyAllWindows()
