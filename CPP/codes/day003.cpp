//
//  day003.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/1/24.
//

#include <stdio.h>

#include "toc.h"

using namespace cv;

/* Day003-OpenCV中图像对象创建与赋值
C++中Mat对象与创建 - clone, copyTo, zeros, ones, eye
 */
namespace Day003 {
    void mainFunction(){
        Mat src = imread("./data/images/test.png");
        
        // 克隆
        Mat m1 = src.clone();
        
        // 复制
        Mat m2;
        src.copyTo(m2);
        
        // 赋值,与src共用data block，修改m3，src也会被改变
        Mat m3 = src;
        
        // CV_8UC3 表示8-bit Unsigned 3-channel
        // CV_16SC1 表示16-bit Unsigned 1-channel
        Mat m4 = Mat::zeros(100, 100, CV_8UC3);
        Mat m5 = Mat::zeros(Size(100, 100), CV_8UC1);
        Mat m6 = Mat::zeros(src.size(), src.type());
        
        Mat m7 = Mat::ones(100, 100, CV_8UC2);
        Mat m8 = Mat::eye(100, 100, CV_8UC3);
        
        Mat kernel = (Mat_<char>(3, 3) << 0, -1, 0,
                      -1, 5, -1,
                      0, -1, 0);
        
        printf("hello\n");
    }
}
