'''
Author       : Bingqiang Zhou
Date         : 2021-09-10 17:00:07
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-10 18:00:07
Description  : 案例四 - 绿幕抠图
    算法基本思想说明：
        1. 将输入图像转换为HSV色彩空间，inRange实现mask的提取
        2. 通过一些简单的图像处理比如形态学开闭操作得到完整的mask区域
        3. 运用高斯模糊生成权重系数
        4. 对绿幕图像与背景图像重新融合生成一个新输出图像，完成抠图
'''

import cv2 as cv
import numpy as np

# 在绿幕中提取前景对象带有权重的mask
def extract_fg_weight_mask_from_green_bg(image):
    # 将图像转到hsv空间
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # 获取到前景mask
    bg_mask = cv.inRange(hsv, (35, 43, 46), (155, 255, 255))
    fg_mask = 255 -bg_mask
    
    # 腐蚀前景mask
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    fg_mask = cv.morphologyEx(fg_mask, cv.MORPH_ERODE, kernel)

    # 对腐蚀的前景mask，进行高斯模糊，并归一化，得到带有权重mask
    fg_wright_mask = cv.GaussianBlur(fg_mask, (3, 3), 0, 0) / 255.0
    return np.expand_dims(fg_wright_mask, axis=-1) # (h, w) -> (h, w, 1), 为后续前背景融合，满足广播机制做准备

# 前背景融合
def blend(fg, bg, fg_weight_mask=0.5):
    h, w = fg.shape[:2]
    bg = cv.resize(bg, (w, h))
    blend_img = (fg*fg_weight_mask + bg*(1-fg_weight_mask)).astype(np.uint8)
    return blend_img

# 读取前背景视频
fg_cap = cv.VideoCapture("./videos/fg.mp4")
bg_cap = cv.VideoCapture("./videos/bg.mp4")

# 读取用作背景的图片
bg_img = cv.imread("./images/bg.jpg")

while True:

    # 读取前景视频帧
    ret, fg_frame = fg_cap.read()
    if ret is False:
        break
    
    # 在绿幕中提取前景对象带有权重的mask
    fg_weight_mask = extract_fg_weight_mask_from_green_bg(fg_frame)
    
    # 读取背景视频帧，如何背景视频比前景视频帧提前结束，则使用最后一帧作为背景
    ret, bg_frame = bg_cap.read()
    if ret is False:
        bg_frame = last_bg_frame
    else:
        last_bg_frame = bg_frame

    cv.imshow("origional", fg_frame) # 源视频
    cv.imshow("blend with image", blend(fg_frame, bg_img, fg_weight_mask)) # 与背景图像融合的视频
    cv.imshow("blend with video", blend(fg_frame, bg_frame, fg_weight_mask)) # 与背景视频帧融合的视频
    
    k = cv.waitKey(50)
    if k == 27:
        break

cv.destroyAllWindows()
