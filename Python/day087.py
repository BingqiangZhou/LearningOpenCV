'''
Author       : Bingqiang Zhou
Date         : 2021-08-29 15:28:22
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-08-29 16:32:02
Description  : 视频分析 – 基于帧差法实现移动对象分析
    光流跟踪与背景消除都是基于建模方式的视频分析方法，其实这类方法最原始的一个例子就是对视频移动对象的帧差法跟踪，
    这个在视频分析与处理中也是一种很常见的手段，有时候会取得意想不到的好效果，帧差法进一步划分有可以分为
        - 两帧差
        - 三帧差
    假设有当前帧frame， 前一帧prev1，更前一帧prev2
    两帧差方法直接使用前一帧 减去当前帧 
        diff = frame – prev1
    三帧差方法计算如下：
        diff1 = prev1 – prev2
        diff2 = frame – prev1
        diff = diff1 & diff2
    帧差法在求取帧差之前一般会进行高斯模糊，用以减低干扰，通过得到的diff图像进行形态学操作，用以合并与候选区域，提升效率。
    帧差法的缺点有如下：
        1. 高斯模糊是高耗时计算
        2. 容易受到噪声与光线干扰
'''

import cv2 as cv
import numpy as np

# 预处理
def post_process(image):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.GaussianBlur(image, (0, 0), 15)
    return image

# 两帧差
def process_two_frame(cur_frame, prev_frame1):
    prev_frame1 = post_process(prev_frame1)
    cur_frame = post_process(cur_frame)

    diff = cv.subtract(cur_frame, prev_frame1)
    ret, binary = cv.threshold(diff, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY)
    k = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
    result = cv.morphologyEx(binary, cv.MORPH_OPEN, k)
    return result

# 三帧差
def process_three_frame(cur_frame, prev_frame1, prev_frame2):
    cur_frame = post_process(cur_frame)
    prev_frame1 = post_process(prev_frame1)
    prev_frame2 = post_process(prev_frame2)

    diff1 = cv.subtract(prev_frame1, prev_frame2)
    diff2 = cv.subtract(cur_frame, prev_frame1)
    ret, binary1 = cv.threshold(diff1, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY)
    ret, binary2 = cv.threshold(diff2, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY)
    diff = cv.bitwise_and(binary1, binary2)
    k = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
    result = cv.morphologyEx(diff, cv.MORPH_OPEN, k)
    return result

capture = cv.VideoCapture("../data/videos/bike.avi")
success, prev_frame1 = capture.read()
prev_frame2 = prev_frame1.copy() # 初始化

result = np.zeros((prev_frame1.shape[0], prev_frame1.shape[1]*3), dtype=prev_frame1.dtype)

while True:
    success, cur_frame = capture.read()
    if not success:
        break

    # 两帧差
    two_frame_diff = process_two_frame(cur_frame, prev_frame1)
    
    # 三帧差
    three_frame_diff = process_three_frame(cur_frame, prev_frame1, prev_frame2)

    # 可视化
    cur_frame_gray = cv.cvtColor(cur_frame, cv.COLOR_BGR2GRAY)
    result[:, :cur_frame.shape[1]] = cur_frame_gray
    result[:, cur_frame.shape[1]:cur_frame.shape[1]*2] = two_frame_diff
    result[:, cur_frame.shape[1]*2:] = three_frame_diff
    cv.imshow("result", result)

    prev_frame2 = prev_frame1
    prev_frame1 = cur_frame

    key = cv.waitKey(50)
    if key == 27:
        break

capture.release()
cv.destroyAllWindows()
        
