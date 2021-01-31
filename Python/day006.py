'''
Author       : Bingqiang Zhou
Date         : 2021-01-31 17:36:32
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-01-31 18:03:17
Description  : LUT(Look Up Table, 查找表)的作用与用法
    applyColorMap(src, dst, COLORMAP)
        - src 表示输入图像
        - dst表示输出图像
        - 匹配到的颜色LUT
    主要用途：颜色匹配、伪色彩增强
    支持以下22种colormap：
        01. COLORMAP_AUTUMN            
        02. COLORMAP_BONE              
        03. COLORMAP_JET
        04. COLORMAP_WINTER
        05. COLORMAP_RAINBOW
        06. COLORMAP_OCEAN
        07. COLORMAP_SUMMER
        08. COLORMAP_SPRING
        09. COLORMAP_COOL
        10. COLORMAP_HSV
        11. COLORMAP_PINK
        12. COLORMAP_HOT
        13. COLORMAP_PARULA
        14. COLORMAP_MAGMA
        15. COLORMAP_INFERNO
        16. COLORMAP_PLASMA
        17. COLORMAP_VIRIDIS
        18. COLORMAP_CIVIDIS
        19. COLORMAP_TWILIGHT
        20. COLORMAP_TWILIGHT_SHIFTED
        21. COLORMAP_TURBO
        22. COLORMAP_DEEPGREEN
    参考链接：https://docs.opencv.org/master/d3/d50/group__imgproc__colormap.html#ga9a805d8262bcbe273f16be9ea2055a65
    22种颜色效果可查看：https://cloud.tencent.com/developer/article/1582400
'''

import cv2 as cv

# src = cv.imread("../data/images/canjian.jpg")
src = cv.imread("../data/images/cos.jpg")

for i in range(22):
    dst = cv.applyColorMap(src, i)
    cv.imshow("image: {}".format(i), dst)

cv.waitKey(0)
cv.destroyAllWindows()


