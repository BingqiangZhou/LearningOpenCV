//
//  day007.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/1/31.
//

#include <stdio.h>

#include "toc.h"

using namespace cv;

/* Day007-图像像素的逻辑操作
 - bitwise_and 与
 - bitwise_xor 异或
 - bitwise_or  或
 上面三个类似，都是针对两张图像的位操作

 - bitwise_not 非
 针对输入图像, 图像取反操作，二值图像分析中经常用
 */
namespace Day007 {
    void mainFunction(){
        Mat m1 = Mat::zeros(300, 300, CV_8UC3);
        Mat m2 = Mat::zeros(300, 300, CV_8UC3);
        
        // 初始化 矩阵（矩形左上角横坐标，矩形左上角纵坐标，宽、高）
        Rect r1(100, 100, 100, 100);
        Rect r2(150, 150, 100, 100);
        
        m1(r1) = Scalar(0, 0, 255); // 红色（bgr）
        m2(r2) = Scalar(0, 255, 255); // 黄色
        
        imshow("m1", m1);
        imshow("m2", m2);
        
        Mat dst;
        
        // 与
        bitwise_and(m1, m2, dst);
        imshow("bitwise_and", dst);
    
        // 或
        bitwise_or(m1, m2, dst);
        imshow("bitwise_or", dst);
        
        // 异或
        bitwise_xor(m1, m2, dst);
        imshow("bitwise_xor", dst);
        
        // 非
        bitwise_not(m2, dst);
        imshow("bitwise_not", dst);
        
        Mat src = imread("./data/images/cos.jpg");
        bitwise_not(src, dst);
        imshow("src bitwise_not", dst);
        
        waitKey(0);
    }
}
