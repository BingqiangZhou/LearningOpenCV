//
//  day031.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/15.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day031-图像梯度 – Sobel算子
 卷积的作用除了实现图像模糊或者去噪，还可以寻找一张图像上所有梯度信息，这些梯度信息是图像的最原始特征数据，
 进一步处理之后就可以生成一些比较高级的特征用来表示一张图像实现基于图像特征的匹配，图像分类等应用。
 Sobel算子是一种很经典的图像梯度提取算子，其本质是基于图像空间域卷积，背后的思想是图像一阶导数算子的理论支持。
 
 Sobel算子X方向  Y方向
 -1 0 +1     -1 -2 -1
 -2 0 +2     0  0  0
 -1 0 +1     +1 +2 +1

 Scharr算子X方向  Y方向
 -3 0 +3     -3 -10 -3
 -10 0 +10     0  0  0
 -3 0 +3     +3 +10 +3
 
 OpenCV实现了基于Sobel算子提取图像梯度的API，表示与解释如下：
     void cv::Sobel(
     InputArray src, // 输入图像
     OutputArray dst, // 输出结果
     int ddepth, // 图像深度CV_32F
     int dx,// 1，X方向 一阶导数
     int dy, // 1，Y方向 一阶导数
     int ksize = 3, // 窗口大小
     double scale = 1, // 放缩比率，1 表示不变
     double delta = 0, // 对输出结果图像加上常量值
     int borderType = BORDER_DEFAULT
     )
 参考：
     https://blog.csdn.net/zaishuiyifangxym/article/details/89840396
     https://blog.csdn.net/swj110119/article/details/51777422
 */
namespace Day031 {
    void mainFunction(){
        Mat src = imread("./data/images/lena.jpg");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        
        imshow("input", src);

        Mat grad_x, grad_y;
        Mat dst;
        
        // Sobel算子
        Sobel(src, grad_x, CV_32F, 1, 0, 3, 1, 0, BORDER_DEFAULT); // x方向
        Sobel(src, grad_y, CV_32F, 0, 1, 3, 1, 0, BORDER_DEFAULT); // y方向
        
        convertScaleAbs(grad_x, grad_x);
        convertScaleAbs(grad_y, grad_y);

        add(grad_x, grad_y, dst, Mat(), CV_16S);
        convertScaleAbs(dst, dst);
        imshow("Sobel gradient x", grad_x);
        imshow("Sobel gradient y", grad_y);
        imshow("Sobel gradient xy", dst);
        
        // Scharr算子
        Scharr(src, grad_x, CV_32F, 1, 0, 3); // x方向
        Scharr(src, grad_y, CV_32F, 0, 1, 3); // y方向
        
        convertScaleAbs(grad_x, grad_x);
        convertScaleAbs(grad_y, grad_y);

        add(grad_x, grad_y, dst, Mat(), CV_16S);
        convertScaleAbs(dst, dst);
        imshow("Scharr gradient x", grad_x);
        imshow("Scharr gradient y", grad_y);
        imshow("Scharr gradient xy", dst);

        waitKey(0);

    }
}
