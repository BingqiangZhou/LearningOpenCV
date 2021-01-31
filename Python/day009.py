'''
Author       : Bingqiang Zhou
Date         : 2021-02-01 01:24:40
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-01 02:11:16
Description  : 图像色彩空间转换
    色彩空间与色彩空间转换
    - RGB色彩空间  (red, green, blue)
    - HSV色彩空间  (Hue色调, Saturation饱和度, Value明度)，参考：https://zh.wikipedia.org/zh-hans/HSL和HSV色彩空间
    - YUV色彩空间  (Y 明亮度（Luminance、Luma），U和V則是色度（Chrominance、Chroma)参考：https://zh.wikipedia.org/wiki/YUV
    - YCrCb色彩空间 是YUV压缩和偏移的版本，参考：https://zh.wikipedia.org/wiki/YCbCr

    API知识点
    - 色彩空间转换cvtColor
    - 提取指定色彩范围区域inRange
'''

import cv2 as cv

src = cv.imread("../data/images/cos.jpg")
cv.imshow("bgr", src)
        
# BGR to RGB
dst = cv.cvtColor(src, cv.COLOR_BGR2RGB)
cv.imshow("rgb", dst)

# BGR to HSV
dst = cv.cvtColor(src, cv.COLOR_BGR2HSV)
cv.imshow("hsv", dst)

# BGR to YUV
cv.cvtColor(src, cv.COLOR_BGR2YUV)
cv.imshow("yuv", dst)

# BGR to YCrCb
cv.cvtColor(src, cv.COLOR_BGR2YCrCb);
cv.imshow("ycrcb", dst)

# 提取指定色彩范围区域inRange
src2 = cv.imread("../data/images/greenback.png")
cv.imshow("src2", src2)
cv.cvtColor(src2, cv.COLOR_BGR2HSV)
mask = cv.inRange(src2, (35, 43, 46), (99, 255, 255)) # 提取绿色和青色部分作为mask
cv.imshow("mask", mask)

# 利用mask将图片中的人提取出来
src2[mask == 255] = 0
cv.imshow("dst", src2)

cv.waitKey(0)
cv.destroyAllWindows()


