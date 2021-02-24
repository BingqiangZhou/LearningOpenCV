'''
Author       : Bingqiang Zhou
Date         : 2021-02-24 22:59:27
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-25 00:50:48
Description  : 图像透视变换应用
    对于很多的文本扫描图像，有时候因为放置的原因导致ROI区域倾斜，
    这个时候我们会想办法把它纠正为正确的角度视角来，方便下一步的布局分析与文字识别，
    这个时候通过透视变换就可以取得比较好的裁剪效果，一步就可以实现裁剪与调整。
    使用透视变换相关几何变换的好处如下：
        1.	透视变换不会涉及到几何变换角度旋转
        2.	透视变换对畸变图像有一定的展开效果
        3.	透视变换可以完成对图像ROI区域提取
    void cv::warpPerspective(
		cv::InputArray src, // 输入图像
		cv::OutputArray dst, // 输出图像
		cv::InputArray M, // 3x3 变换矩阵
		cv::Size dsize, // 目标图像大小
		int flags = cv::INTER_LINEAR, // 插值方法
		int borderMode = cv::BORDER_CONSTANT, // 外推方法
		const cv::Scalar& borderValue = cv::Scalar() //常量边界时使用
    )
    透视变换(Perspective Transformation)是将成像投影到一个新的视平面(Viewing Plane)，
    也称作投影映射(Projective Mapping)。
    参考链接:
        透视变换——cv::getPerspectiveTransform()与cv::warpPerspective()详解 - https://blog.csdn.net/guduruyu/article/details/72518340
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# src = cv.imread("../data/images/st01.jpg")
src = cv.imread("../data/images/st02.png")

# 提取mask
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
thresh, mask = cv.threshold(gray, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY_INV)

# 获取最小矩形轮廓的四个边缘点
contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
rect = cv.minAreaRect(contours[0])
box = cv.boxPoints(rect)

# for i, pt in enumerate(box):
#     cv.putText(src, str(i), tuple(np.int0(pt)), cv.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 2)

w, h = np.array(rect[1])
# 映射坐标一一对应，左下角顺时针顺序
dst_box = np.array([
    [0, h], # 右下角
    [0, 0], # 左下角
    [w, 0], # 左上角
    [w, h]  # 右上角
])
print(rect, box, dst_box, sep='\n')

# 透视变换矩阵M
# m, status = cv.findHomography(box, dst_box)
m = cv.getPerspectiveTransform(box.astype(np.float32), dst_box.astype(np.float32))
# 透视变换
result = cv.warpPerspective(src, m, (int(w), int(h)))
if h < w:
    result = cv.rotate(result, cv.ROTATE_90_CLOCKWISE)

# 可视化
rows = 1
cols = 3
images = [src, mask, result]
titles = ["original image", "mask", "result"]
plt.figure(figsize=(cols * 4, rows * 3)) # Width, height in inches.
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
