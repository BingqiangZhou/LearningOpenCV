'''
Author       : Bingqiang Zhou
Date         : 2021-02-15 20:58:16
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-15 21:51:23
Description  : 图像金字塔
    图像金字塔概念
        图像金字塔是对一张输入图像先模糊再下采样为原来大小的1/4（宽高缩小一半）、
        不断重复模糊与下采样的过程就得到了不同分辨率的输出图像，叠加在一起就形成了图像金字塔、
        所以图像金字塔是图像的空间多分辨率存在形式。
        这里的模糊是指高斯模糊，所以这个方式生成的金字塔图像又称为高斯金字塔图像。
    
    高斯金字塔图像有两个基本操作
        reduce 是从原图生成高斯金字塔图像、生成一系列低分辨图像
        expand是从高斯金字塔图像反向生成高分辨率图像

    规则：
        1.	图像金字塔在redude过程或者expand过程中必须是逐层
        2.	默认情况：reduce过程中每一层都是前一层的1/4（宽高缩小一半），expand过程中每一层都是前一层的4倍（宽高扩大一倍）

    相关API
        reduce 操作 pyrDown
        expand操作 pyrUp
'''

import cv2 as cv

def image_pyramid(src, level=3, upsample=False):
    pyramid_images = []
    temp = src
    for i in range(level):
        if upsample is False:
            dst = cv.pyrDown(temp)
        else:
            dst = cv.pyrUp(temp)
        pyramid_images.append(dst)
        temp = dst
    return pyramid_images

src = cv.imread("../data/images/lena.jpg")

# 图像金字塔 reduce操作
down_pyramid = image_pyramid(src, upsample=False)

# 图像金字塔 expand操作
up_pyramid = image_pyramid(src, upsample=True)

# 可视化
images = [src]
images.extend(down_pyramid)
images.extend(up_pyramid)
titles = ["original image"]
titles.extend([f"down_pyramid {i+1}" for i in range(len(down_pyramid))])
titles.extend([f"up_pyramid {i+1}" for i in range(len(up_pyramid))])

for index, image in enumerate(images):
    cv.imshow(titles[index], image)
    print(titles[index], image.shape) 

cv.waitKey(0)