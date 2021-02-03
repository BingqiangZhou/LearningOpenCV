'''
Author       : Bingqiang Zhou
Date         : 2021-02-03 12:27:35
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-03 15:03:34
Description  : 图像ROI与ROI操作
    图像的ROI(region of interest)是指图像中感兴趣区域、在OpenCV中图像设置图像ROI区域，实现只对ROI区域操作。

    1. 矩形ROI区域提取
    2. 矩形ROI区域copy
    3. 不规则ROI区域
        - ROI区域mask生成
        - 像素位 and操作
        - 提取到ROI区域
        - 加背景or操作
        - add 背景与ROI区域
'''

import cv2 as cv
import numpy as np


src = cv.imread("../data/images/cos.jpg")
cv.imshow("source image", src)

# 提取ROI区域，将图像最中心的200x200区域作为ROI
h, w = src.shape[:2]
cx = w // 2 # 图像中心点的x坐标
cy = h // 2 # 图像中心点的y坐标
roi = src[cy - 100: cy + 100, cx - 100: cx + 100]
cv.imshow("roi 200x200", roi)

# roi依旧指向src对应的内存空间，对roi进行修改，则src也会被修改
roi[:] = [0, 0, 255]
cv.imshow("roi (0, 0, 255) image", src)

# 复制roi，将roi与src对应的内存空间脱离，roi拥有对立的内存空间，对roi进行修改，则src不再会被修改
roi_new = np.copy(roi)
roi_new[:] = [255, 0, 0]
cv.imshow("roi_new image", src)

green_background_image = cv.imread("../data/images/greenback.png")
cv.imshow("green background image", green_background_image)

## 生成mask
hsv = cv.cvtColor(green_background_image, cv.COLOR_BGR2HSV)
mask = cv.inRange(green_background_image, (35, 43, 46), (99, 255, 255)) # 提取绿色（35-77，43-255，46-255）与青色（78-99，43-255，46-255）区域
cv.imshow("mask", mask)

# 直接将背景（除人以外的区域的绿色和青色区域）改为红色
temp = np.copy(green_background_image)
temp[mask == 255] = [0, 0, 255]
cv.imshow("change green background", temp)

## 提取人的区域mask
person_mask = cv.bitwise_not(mask)
# person_mask = 255 - mask # 等价于上一行代码
cv.imshow("person mask", person_mask)

## 获取彩色人形区域
# person_image = cv.bitwise_or(green_background_image, green_background_image, mask=person_mask) # 等同于下面的bitwise_and
person_image = cv.bitwise_and(green_background_image, green_background_image, mask=person_mask) # 等同于下面两行代码，将背景设置为黑色
# person_image = np.copy(green_background_image)
# person_image[mask == 255] = [0, 0, 0]
cv.imshow("person image", person_image)

## 生成新的背景
new_background = np.zeros(green_background_image.shape, dtype=np.uint8)
new_background[:] = [0, 255, 255] # 黄色背景

## 读取图像作为背景
# new_background = cv.imread("../data/images/cos.jpg")
# size = green_background_image.shape[:2][::-1] # 需要注意的是numpy中shape是(h, w,……)，而opencv中size是(cols, rows)即(w, h)，因此这里做了一下翻转
# new_background = cv.resize(new_background, size, interpolation=cv.INTER_LINEAR)
cv.imshow("new background", new_background)

## 将背景中的人形部分去除
# background_without_person_region = cv.bitwise_and(new_background, new_background, mask=mask) # 等同于下面的bitwise_or
background_without_person_region = cv.bitwise_or(new_background, new_background, mask=mask) # 等同于下面两行代码，将人形部分设置为黑色
# background_without_person_region = np.copy(new_background)
# background_without_person_region[person_mask == 255] = [0, 0, 0]
cv.imshow("background_without_person_region", background_without_person_region)

## 合并新的背景和人形区域
new_image = cv.add(background_without_person_region, person_image) # 将去除人形部分的背景区域与彩色人形区域相加
# new_image = new_background + person_image 与上一行代码等效
cv.imshow("new image", new_image)

cv.waitKey(0)
cv.destroyAllWindows()