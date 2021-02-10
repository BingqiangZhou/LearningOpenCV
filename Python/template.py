'''
Author       : Bingqiang Zhou
Date         : 2021-02-10 19:26:53
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-10 19:37:16
Description  : template
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/lena.jpg")

# 可视化
rows = 1
cols = 2
plt.subplot(rows, cols, 1)
plt.title("src")
plt.imshow(src[:, :, ::-1])
plt.show()