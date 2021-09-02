'''
Author       : Bingqiang Zhou
Date         : 2021-09-02 15:11:06
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-02 15:59:17
Description  : 二维码检测与识别
    OpenCV3.4.4以上版本与OpenCV4.0版本支持该功能！
    OpenCV在对象检测模块中QRCodeDetector有两个相关API分别实现二维码检测与二维码解析
    bool cv::QRCodeDetector::detect(
        InputArray img,
        OutputArray points 
    )const
    img输入图像，灰度或者彩色图像
    points 得到的二维码四个点的坐标信息

    解析二维码！
    std::string cv::QRCodeDetector::decode(
        InputArray img,
        InputArray points,
        OutputArray straight_qrcode = noArray() 
    )
    img输入图像，灰度或者彩色图像
    points 二维码ROI最小外接矩形顶点坐标
    qrcode 输出的是二维码区域ROI图像信息
    返回的二维码utf-8字符串
    上述两个API功能，可以通过一个API调用实现，该API如下：
    std::string cv::QRCodeDetector::detectAndDecode(
        InputArray img,
        OutputArray points = noArray(),
        OutputArray straight_qrcode = noArray() 
    )

    拓展资料：
        官方文档 cv::QRCodeDetector Class Reference：https://docs.opencv.org/3.4/de/dc3/classcv_1_1QRCodeDetector.html
'''

import cv2 as cv
import numpy as np

# qrcode_img = cv.imread("../data/images/qrcode_05.jpg") # 二维码中包含中文，QRCodeDetector不支持中文
qrcode_img1 = cv.imread("../data/images/qrcode_06.jpg")
qrcode_img2 = cv.imread("../data/images/qrcode_07.png")

qrcode_detector = cv.QRCodeDetector()
ret, points1 = qrcode_detector.detect(qrcode_img1)
if ret:
    # print(points)
    result_str1, straight_qrcode = qrcode_detector.decode(qrcode_img1, points1)
    cv.polylines(qrcode_img1, points1.astype(np.int), True, (0, 255, 0), 2)
    # putText的坐标是左下角坐标
    cv.putText(qrcode_img1, result_str1, (0, 20), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1) 
    # print(result_str1, points1)

result_str2, points2, straight_qrcode = qrcode_detector.detectAndDecode(qrcode_img2)
cv.polylines(qrcode_img2, points2.astype(np.int), True, (0, 255, 0), 2)
# putText的坐标是左下角坐标
cv.putText(qrcode_img2, result_str1, (0, 20), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1) 
# print(result_str2, points2)

cv.imshow("qrcode1", qrcode_img1)
cv.imshow("qrcode2", qrcode_img2)
cv.waitKey(0)
cv.destroyAllWindows()
