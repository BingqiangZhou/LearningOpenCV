'''
Author       : Bingqiang Zhou
Date         : 2021-02-10 19:26:53
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-11 15:17:53
Description  : template
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/lena.jpg")

# 可视化
rows = 1
cols = 2
images = [src]
titles = ["original image"]
for index, image in enumerate(images):
    plt.subplot(rows, cols, index + 1)
    if index >= len(titles):
        plt.title("image")
    else:
        plt.title(titles[index])
    plt.axis("off")
    plt.imshow(image[:, :, ::-1])
plt.show()