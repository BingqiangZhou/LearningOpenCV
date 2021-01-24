//
//  day005.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/1/24.
//

#include <stdio.h>

#include "toc.h"

using namespace cv;

/* Day005-图像像素的算术操作
 加add、减subtract、乘multiply、除divide
 防止数据溢出 saturate_cast
 注意点：图像的数据类型、通道数目、大小必须相同
 */
namespace Day005 {
    void mainFunction(){
        Mat m1 = imread("./data/images/linux_logo.jpg");
        Mat m2 =  imread("./data/images/windows_logo.jpg");
//        Mat m1 = imread("./data/images/linux_logo.jpg", IMREAD_GRAYSCALE);
//        Mat m2 =  imread("./data/images/windows_logo.jpg", IMREAD_GRAYSCALE);
//        Mat m2 =  imread("./data/images/test.png");
        
        if(m1.empty() || m2.empty()){
            printf("could not load image...\n");
            return ;
        }
        
        // 图像的数据类型、通道数目、大小必须相同
        if(m1.size() != m2.size() || m1.type() != m2.type()){
            printf("could not perfrom operate...\n");
            return ;
        }
        
        Mat result = Mat::zeros(m1.size(), m1.type());
        
        // 加
        add(m1, m2, result);
        imshow("add", result);
        
        // 减
        subtract(m1, m2, result);
        imshow("subtract", result);
        
        // 乘
        multiply(m1, m2, result);
        imshow("multiply", result);
        
        // 除
        divide(m1, m2, result);
        imshow("divide", result);
        
        // 自行实现加操作(数组遍历)
        addImplementByArray(m1, m2, result);
        imshow("addImplementByArray", result);
        
        // 自行实现加操作（指针遍历）
        addImplementByPointer(m1, m2, result);
        imshow("addImplementByPointer", result);
        
        waitKey(0);
        
    };
    // 自行实现加操作(数组遍历)
    void addImplementByArray(Mat m1, Mat m2, Mat result){
        
        // 图像的数据类型、通道数目、大小必须相同
        if(m1.size() != m2.size() || m1.type() != m2.type()){
            printf("could not perfrom operate...\n");
            return ;
        }
        
        int h = m1.rows;
        int w = m1.cols;
        int c = m1.channels();
        
        int v1 = 0, v2 = 0;
        
        for (int row = 0; row < h; row++) {
            for (int col = 0; col < w; col++) {
                if(c == 3){
                    for (int i = 0; i < c; i++) {
                        v1 = m1.at<Vec3b>(row, col)[i];
                        
                        v2 = m2.at<Vec3b>(row, col)[i];
                        
                        result.at<Vec3b>(row, col)[i] = saturate_cast<uchar>(v1 + v2);
                    }
                    
                    // Vec 重载了运算符，可以直接加减乘除, 但无法使用saturate_cast防止溢出，saturate_cast不支持Vec
//                    result.at<Vec3b>(row, col) = m1.at<Vec3b>(row, col) + m2.at<Vec3b>(row, col);
                }else if (c == 1){
                    result.at<uchar>(row, col) = saturate_cast<uchar>(m1.at<uchar>(row, col) + m2.at<uchar>(row, col));
                    
                    
                    //                    result.at<uchar>(row, col) = m1.at<uchar>(row, col) + m2.at<uchar>(row, col);
                    // 第99行 直接相加，不使用saturate_cast不会报错，但数值被截断，但显示的图像与调用saturate_cast（防止数据溢出）的图像h会不一样。
                    // saturate_cast 相当于 if(data < 0) data = 0; else if(data > 255) data = 255;
                    // 第99行代码相当于强制截断，只取最低的8位,例如254(1111 1110)+105(0110 1001)=359(1 0110 0111)，强制截断得到103(0110 0111)
//                    if(m1.at<uchar>(row, col) + m2.at<uchar>(row, col) > 255){
//                        printf("%d, %d, %d \n", m1.at<uchar>(row, col), m2.at<uchar>(row, col), result.at<uchar>(row, col));
//                        break;
//                    }
                }
            }
        }
    };
    // 自行实现加操作（指针遍历）
    void addImplementByPointer(cv::Mat m1, cv::Mat m2, cv::Mat result)
    {
        // 图像的数据类型、通道数目、大小必须相同
        if(m1.size() != m2.size() || m1.type() != m2.type()){
            printf("could not perfrom operate...\n");
            return ;
        }
        
        int h = m1.rows;
        int w = m1.cols;
        int c = m1.channels();
        
        for (int row = 0; row < h; row++) {
            uchar* curr_p1 = m1.ptr<uchar>(row); // 获取到当前行的首地址
            uchar* curr_p2 = m2.ptr<uchar>(row);
            uchar* curr_p3 = result.ptr<uchar>(row);
            
            for (int col = 0; col < w; col++) {
                for (int i = 0; i < c; i++){
                    *curr_p3++ = saturate_cast<uchar>(*curr_p1++ + *curr_p2++);
                }
            }
        }
    }
}
