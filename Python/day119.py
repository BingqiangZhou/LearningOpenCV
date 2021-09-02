'''
Author       : Bingqiang Zhou
Date         : 2021-09-02 14:29:39
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-02 15:00:39
Description  : Grabcut图像分割 – 背景替换
    使用Grabcut实现图像对象提取，通过背景图像替换，实现图像合成，通过对背景图像高斯模糊实现背景虚化效果，
    完整的步骤如下：
    1. ROI区域选择
    2. Grabcut对象分割
    3. Mask生成
    4. 使用mask，实现背景与前景的高斯权重融合
'''

import cv2 as cv
import numpy as np

img = cv.imread("../data/images/master.jpg") # (640, 512, 3)
h, w = img.shape[:2]
new_bg = cv.imread("../data/images/river.jpg") # (533, 801, 3)
new_bg = cv.resize(new_bg, (w, h))
print(img.shape, new_bg.shape)
rect = cv.selectROI("select roi", img, showCrosshair=True) # 交互选取分割目标区域

# 初始化mask 以及 前背景模型
bgdModel = np.zeros((1, 65), dtype=np.float64)
fgdModel = np.zeros((1, 65), dtype=np.float64)
mask = np.zeros(img.shape[:2], dtype=np.uint8)

# grabcut分割
mask, bgdModel, fgdModel = cv.grabCut(img, mask, rect, bgdModel, fgdModel, 6, cv.GC_INIT_WITH_RECT)
fg_mask = np.where((mask == 1) + (mask == 3), 255, 0).astype(np.uint8)

# 使用mask，实现背景与前景的高斯权重融合
k = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
fg_mask = cv.morphologyEx(fg_mask, cv.MORPH_DILATE, k)
w = cv.GaussianBlur(fg_mask, (5, 5), 0)[:, :, None] / 255.0 # (h, w, 1)
new_img = ((1 - w) * new_bg + w * img).astype(np.uint8)

# 提取分割得到的前景对象
result = cv.bitwise_and(img, img, mask=fg_mask)

# 可视化
cv.imshow("result", result)
cv.imshow("new_img", new_img)
cv.waitKey(0)
cv.destroyAllWindows()
