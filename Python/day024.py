'''
Author       : Bingqiang Zhou
Date         : 2021-02-11 13:15:30
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-11 14:08:08
Description  : 图像噪声
    图像噪声产生的原因很复杂，有的可能是数字信号在传输过程中发生了丢失或者受到干扰，
        有的是成像设备或者环境本身导致成像质量不稳定，反应到图像上就是图像的亮度与颜色呈现某种程度的不一致性。
    从噪声的类型上，常见的图像噪声可以分为如下几种:
        - 椒盐噪声， 
        是一种随机在图像中出现的稀疏分布的黑白像素点， 对椒盐噪声一种有效的去噪手段就是图像中值滤波

        - 高斯噪声/符合高斯分布
        一般会在数码相机的图像采集(acquisition)阶段发生,这个时候它的物理/电/光等各种信号都可能导致产生高斯分布噪声。

        - 均匀分布噪声
        均匀/规则噪声一般都是因为某些规律性的错误导致的
    代码演示
    - 图像椒盐噪声生成
    - 图像高斯噪声生成
'''

import cv2 as cv
import numpy as np

# 图像椒盐噪声生成
def generate_salt_pepper_noise(image):
    dst = np.copy(image)
    h, w = dst.shape[:2]
    nums = 1000 # 产生椒盐噪声的点数
    x = np.random.randint(0, w, nums) # 随机x坐标
    y = np.random.randint(0, h, nums) # 随机y坐标
    for index, pos in enumerate(zip(y, x)):
        # 产生白噪声或者黑噪声
        if index % 2 == 0:
            dst[pos] = 255
        else:
            dst[pos] = 0
    return dst

# 图像高斯噪声生成
def generate_gaussian_noise(image):
    noise = np.zeros_like(image)
    mean = (15, 15, 15)
    stddev = (30, 30, 30)
    cv.randn(noise, mean, stddev) # 随机产生高斯噪声
    dst = cv.add(image, noise)
    return dst

src = cv.imread("../data/images/cos.jpg")
dst_salt_pepper = generate_salt_pepper_noise(src) # 图像椒盐噪声生成
dst_gaussian = generate_gaussian_noise(src) # 图像高斯噪声生成

# 可视化，将三张图像和在一起显示
h, w, c = src.shape
image = np.zeros((h, w*3, c), np.uint8)
image[:, :w, :] = src
cv.putText(image, "original image", (10, 30), cv.FONT_HERSHEY_PLAIN, 2.0, (0, 255, 255))
image[:, w : w*2, :] = dst_salt_pepper
cv.putText(image, "salt pepper noise", (w+10, 30), cv.FONT_HERSHEY_PLAIN, 2.0, (0, 255, 255))
image[:, w*2 : w*3, :] = dst_gaussian
cv.putText(image, "gaussian noise", (2*w+10, 30), cv.FONT_HERSHEY_PLAIN, 2.0, (0, 255, 255))
cv.imshow("result", image)

cv.waitKey(0)
cv.destroyAllWindows()