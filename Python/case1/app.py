'''
Author       : Bingqiang Zhou
Date         : 2021-09-08 18:30:54
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-09 00:19:34
Description  : 案例一 – 识别0～9印刷体数字
    实现识别的完整流程
    
    对输入的图像处理如下：
    1.	二值化
    2.	提取字符ROI区域
    3.	对ROI提取特征向量
    4.	对比特征向量，计算L2距离
    5.	最小距离对应的标签即为该字符预测结果
'''

import cv2 as cv
import numpy as np
from utils import extract_feature

def get_feature(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # 反向二值化，将黑色的数字变为白色，白色背景变成黑色
    retval, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU) 
    # 定位到各个数字的RoI区域
    contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    rects = []
    for c in contours:
        rect = cv.boundingRect(c)
        # print(rect)
        rects.append(rect)
        cv.rectangle(img, rect, (0, 0, 255), 1, 8)

    # 按左上角x坐标从小到大排列，如图像td1.png，从左到右排列，分别为1-9、0
    rects = sorted(rects, key=lambda x: x[0], reverse=False)
    feature_list = []
    for i, r in enumerate(rects):
        x, y, w, h = r
        roi = binary[y:y+h, x:x+w]
        feature = extract_feature(roi)
        feature_list.append(feature)
        # print(f"number {(i + 1) % 10} 's features: ", feature)
    return np.array(feature_list), np.array(rects) # (n, 40), (n, 4)

# 提取模版的数字的特征
# template_img = cv.imread("./images/td1.png")
template_img = cv.imread("./images/td2.png")
template_feature, template_rects = get_feature(template_img) # 1-9、0

## 提取测试图像的特征
# test_img = cv.imread("./images/digit-01.png")
test_img = cv.imread("./images/digit-02.png")
test_feature, test_rects = get_feature(test_img)

## 计算特征之间的距离，对应距离最小的模版的数字为预测结果
for i in range(len(test_feature)):
    cur_fea = test_feature[i:i+1] # (1, 40)
    x, y, w, h = test_rects[i]
    dist = np.linalg.norm(cur_fea - template_feature, axis=1)
    index = np.argmin(dist)
    predict_number = int((index + 1) % 10)
    # 可视化 结果
    cv.putText(test_img, str(predict_number), (x, y+h+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))

cv.imshow("template", template_img)
cv.imshow("test_img", test_img)
cv.waitKey(0)
cv.destroyAllWindows()