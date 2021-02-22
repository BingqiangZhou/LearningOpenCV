'''
Author       : Bingqiang Zhou
Date         : 2021-02-22 16:17:25
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-22 17:05:14
Description  : 二值图像分析 – 使用Hu矩实现轮廓匹配
    对图像二值图像的每个轮廓，可以计算轮廓几何矩，根据几何矩可以计算图像的中心位置，
    估计得到中心位置可以计算中心矩、然后再根据中心矩可以计算胡矩。
    OpenCV中可以通过如下的API一次计算出上述三种矩，API如下：
        Moments cv::moments(
            InputArray 	array,
            bool binaryImage = false
        )
    array是输入的图像轮廓点集合
    输出的图像几何矩，根据几何矩输出结果可以计算胡矩，胡矩计算的API如下：
        void cv::HuMoments(
        const Moments & moments,
        double 	hu[7] 
        )
    moments参数表示输入的图像矩
    hu[7]表示输出的胡矩七个值

    然后我们可以使用hu矩作为输入，对轮廓进行匹配，进行轮廓外形匹配的API如下：
        double cv::matchShapes(
            InputArray 	contour1,
            InputArray 	contour2,
            int method,
            double parameter
        )
    contour1第一个轮廓点集合，或者灰度图像
    contour2第二个轮廓点集合，或者灰度图像
    method表示比较方法，最常见有
    CONTOURS_MATCH_I1
    CONTOURS_MATCH_I2
    CONTOURS_MATCH_I3
    Parameter方法声明的参数，OpenCV3.x版本中已经不需要了。
    返回值越小，越相似。
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def find_contours(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    thresh, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)

    # 发现轮廓
    contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return contours

def draw_contours(image, contours):
    rect = cv.minAreaRect(contours) # 获取轮廓最小外接矩形
    box = cv.boxPoints(rect) # 通过矩形的左上角和高宽获得矩形的四个点的坐标
    box = np.int0(box) # int0是intp的别名（alias），根据32位、64位机器对应int32、int64
    cv.drawContours(image, [box], 0, (0, 0, 255), 2, cv.LINE_8) # 绘制矩形框
    return image

src1 = cv.imread("../data/images/abc.png")
src2 = cv.imread("../data/images/a.png")
# src2 = cv.imread("../data/images/a5.png")

# 发现轮廓
contours1 = find_contours(src1)
contours2 = find_contours(src2)

# 计算几何距
mm2 = cv.moments(contours2[0])
# 计算Hu距
hum2 = cv.HuMoments(mm2)

temp = src1.copy()
# 轮廓匹配
for c in range(len(contours1)):

    # 直接匹配轮廓
    dist1 = cv.matchShapes(contours1[c], contours2[0], cv.CONTOURS_MATCH_I1, 0) # 距离越小，越相似
    if dist1 < 1:
        temp = draw_contours(temp, contours1[c])


    mm = cv.moments(contours1[c]) # 计算几何距
    hum = cv.HuMoments(mm) # 计算胡距
    dist2 = cv.matchShapes(hum, hum2, cv.CONTOURS_MATCH_I1, 0) # 距离越小，越相似
    if dist2 < 1:
        src1 = draw_contours(src1, contours1[c])
    
    print(f"contours :{dist1}, hu: {dist2}")
        

# 可视化 
rows = 1
cols = 3
images = [src2, src1, temp]
titles = ["image", "match by HuMoments", "match by contours"]
plt.figure(figsize=(cols * 4, rows * 3)) # Width, height in inches.
for index, image in enumerate(images):
    plt.subplot(rows, cols, index + 1)
    if index >= len(titles):
        plt.title("image")
    else:
        plt.title(titles[index])
    plt.axis("off")
    if image.ndim > 2:
        plt.imshow(image[:, :, ::-1])
    else:
        plt.imshow(image, cmap="gray")
plt.show()
