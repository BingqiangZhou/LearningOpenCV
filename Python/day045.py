'''
Author       : Bingqiang Zhou
Date         : 2021-02-17 17:00:00
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-17 18:07:04
Description  : 图像二值化与去噪
    对于一张需要二值化的图像，我们有两种选择
    选择一
        直接对输入图像转换为灰度图像，然后二值化
    选择二
        首先对输入图像进行降噪，去除噪声干扰，然后再二值化

    在进行去噪声的时候，还记得前面我们分享的几种去噪声方法，可以选择的有
    均值模糊去噪声
    高斯模糊去噪声
    双边/均值迁移模糊去噪声
    非局部均值去噪声
'''

import cv2 as cv
import matplotlib.pyplot as plt

src = cv.imread("../data/images/coins.jpg")
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

# 直接对输入图像转换为灰度图像，然后二值化
threshold, binary = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)
print("THRESH_OTSU threshold: ", threshold)

# 首先对输入图像进行降噪，去除噪声干扰，然后再二值化
# 1. 均值模糊去噪声
blured = cv.blur(src, (3, 3))
blured_gray = cv.cvtColor(blured, cv.COLOR_BGR2GRAY)
threshold, blured_binary = cv.threshold(blured_gray, 0, 255, cv.THRESH_OTSU)
print("THRESH_OTSU blur threshold: ", threshold)

# 2. 高斯模糊去噪声
gaussian_blured = cv.GaussianBlur(src, (3, 3), 0)
gaussian_blured_gray = cv.cvtColor(gaussian_blured, cv.COLOR_BGR2GRAY)
threshold, gaussian_blured_binary = cv.threshold(gaussian_blured_gray, 0, 255, cv.THRESH_OTSU)
print("THRESH_OTSU GaussianBlur threshold: ", threshold)

# 3. 双边模糊去噪声
bilateral_blured = cv.bilateralFilter(src, -1, 100, 10)
bilateral_blured_gray = cv.cvtColor(bilateral_blured, cv.COLOR_BGR2GRAY)
threshold, bilateral_blured_binary = cv.threshold(bilateral_blured_gray, 0, 255, cv.THRESH_OTSU)
print("THRESH_OTSU bilateralFilter threshold: ", threshold)

# 4. 均值迁移模糊去噪声
pyrMeanShiftFiltering_blured = cv.pyrMeanShiftFiltering(src, 10, 100)
pyrMeanShiftFiltering_blured_gray = cv.cvtColor(pyrMeanShiftFiltering_blured, cv.COLOR_BGR2GRAY)
threshold, pyrMeanShiftFiltering_blured_binary = cv.threshold(pyrMeanShiftFiltering_blured_gray, 0, 255, cv.THRESH_OTSU)
print("THRESH_OTSU pyrMeanShiftFiltering threshold: ", threshold)

# 5. 非局部均值去噪声
fastNlMeansDenoisingColored_blured = cv.fastNlMeansDenoisingColored(src)
fastNlMeansDenoisingColored_blured_gray = cv.cvtColor(fastNlMeansDenoisingColored_blured, cv.COLOR_BGR2GRAY)
threshold, fastNlMeansDenoisingColored_binary = cv.threshold(fastNlMeansDenoisingColored_blured_gray, 0, 255, cv.THRESH_OTSU)
print("THRESH_OTSU pyrMeanShiftFiltering threshold: ", threshold)

# 可视化
rows = 2
cols = 4
images = [gray, binary, blured_binary, gaussian_blured_binary, 
        bilateral_blured_binary, pyrMeanShiftFiltering_blured_binary, fastNlMeansDenoisingColored_binary]
titles = ["original image", "THRESH_OTSU", "blur+OTSU", "GaussianBlur+OTSU", 
        "bilateralFilter+OTSU", "pyrMeanShiftFiltering+OTSU", "fastNlMeansDenoisingColored+OTSU"]
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
