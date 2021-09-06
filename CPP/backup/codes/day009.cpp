//
//  day009.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/1.
//

#include <stdio.h>

#include "toc.h"

using namespace cv;
using namespace std;

/* Day009-图像色彩空间转换
 色彩空间与色彩空间转换
 - RGB色彩空间  (red, green, blue)
 - HSV色彩空间  (Hue色调, Saturation饱和度, Value明度)，参考：https://zh.wikipedia.org/zh-hans/HSL和HSV色彩空间
 - YUV色彩空间  (Y 明亮度（Luminance、Luma），U和V則是色度（Chrominance、Chroma)参考：https://zh.wikipedia.org/wiki/YUV
 - YCrCb色彩空间 是YUV压缩和偏移的版本，参考：https://zh.wikipedia.org/wiki/YCbCr

 API知识点
 - 色彩空间转换cvtColor
 - 提取指定色彩范围区域inRange
 */
namespace Day009 {
    void mainFunction(){
        
        Mat src = imread("./data/images/cos.jpg");
        imshow("bgr", src);
        
        Mat dst;
        
        // BGR to RGB
        cvtColor(src, dst, COLOR_BGR2RGB);
        imshow("rgb", dst);
        
        // BGR to HSV
        cvtColor(src, dst, COLOR_BGR2HSV);
        imshow("hsv", dst);
        
        // BGR to YUV
        cvtColor(src, dst, COLOR_BGR2YUV);
        imshow("yuv", dst);
        
        // BGR to YCrCb
        cvtColor(src, dst, COLOR_BGR2YCrCb);
        imshow("ycrcb", dst);
        
        // 提取指定色彩范围区域inRange
        Mat src2 = imread("./data/images/greenback.png");
        imshow("src2", src2);
        cvtColor(src2, dst, COLOR_BGR2HSV);
        Mat mask;
        inRange(src2, Scalar(35, 43, 46), Scalar(99, 255, 255), mask); //提取绿色和青色部分作为mask
        imshow("mask", mask);
        
        // 利用mask将图片中的人提取出来
        bitwise_not(mask, mask); //mask取反，人的区域为1，绿色背景区域为0
        vector<Mat> bgr;
        split(src2, bgr); // 通道分离
        for (Mat channel : bgr) {
            bitwise_and(channel, mask, channel);// 提取人的区域的各个通道的像素值
        }
        merge(bgr, dst);// 通道合并
        imshow("dst", dst);
        
        waitKey(0);
    }
}
