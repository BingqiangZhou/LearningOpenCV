'''
Author       : Bingqiang Zhou
Date         : 2021-02-15 22:26:14
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-15 23:57:44
Description  : 拉普拉斯金字塔
    对输入图像实现金字塔的reduce操作就会生成不同分辨率的图像、对这些图像进行金字塔expand操作，
    然后使用reduce减去expand之后的结果就会得到图像拉普拉斯金字塔图像。

    举例如下：
    输入图像G(0)
    金字塔reduce操作生成 G(1), G(2), G(3)
    拉普拉斯金字塔：
        L0 = G(0)-expand(G(1))
        L1 = G(1)-expand(G(2))
        L2 = G(2)–expand(G(3))

    G(0)减去expand(G(1))得到的结果就是两次高斯模糊输出的不同，所以L0称为DOG（高斯不同）、它约等于LOG所以又称为拉普拉斯金字塔。
    所以要求的图像的拉普拉斯金字塔，首先要进行金字塔的reduce操作，然后在通过expand操作，最后相减得到拉普拉斯金字塔图像。
'''

import cv2 as cv

def laplaian_pyramid(src, level=3):
    gaussian_images = []
    laplaian_pyramid = []
    h, w = src.shape[:2]
    
    # reduce操作(高斯金字塔)
    temp = src.copy()
    for i in range(level):
        dst = cv.pyrDown(temp)
        gaussian_images.append(dst)
        temp = dst
    
    # 拉普拉斯金字塔
    # 生成G0
    h, w = src.shape[:2]
    dst = cv.subtract(src, cv.pyrUp(gaussian_images[0], dstsize=(w, h))) + 127
    laplaian_pyramid.append(dst)
    for i in range(level - 1):
        h, w = gaussian_images[i].shape[:2]
        dst = cv.subtract(gaussian_images[i], cv.pyrUp(gaussian_images[i+1], dstsize=(w, h))) + 127
        laplaian_pyramid.append(dst)
    return laplaian_pyramid

src = cv.imread("../data/images/lena.jpg")

# 图像金字塔 reduce操作
down_pyramid = laplaian_pyramid(src)

# 可视化
images = [src]
images.extend(down_pyramid)
titles = ["original image"]
titles.extend([f"down_pyramid {i+1}" for i in range(len(down_pyramid))])

for index, image in enumerate(images):
    cv.imshow(titles[index], image)
    print(titles[index], image.shape) 

cv.waitKey(0)
