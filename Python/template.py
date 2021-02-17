'''
Author       : Bingqiang Zhou
Date         : 2021-02-10 19:26:53
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-16 00:12:06
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
    if image.ndim > 2:
        plt.imshow(image[:, :, ::-1])
    else:
        plt.imshow(image, cmap="gray")
plt.show()

for index, image in enumerate(images):
    cv.imshow(titles[index], image)
    print(titles[index], image.shape) 

cv.waitKey(0)