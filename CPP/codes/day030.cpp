//
//  day030.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/15.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day030-OpenCV中的自定义滤波器
 图像卷积最主要功能有图像模糊、锐化、梯度边缘等，前面已经分享图像卷积模糊的相关知识点，
 OpenCV除了支持上述的卷积模糊（均值与边缘保留）还支持自定义卷积核，实现自定义的滤波操作。
 自定义卷积核常见的主要是均值、锐化、梯度等算子。下面的三个自定义卷积核分别可以实现卷积的均值模糊、锐化、梯度功能。

 1，    1， 1      0， -1， 0        1， 0
 1，    1， 1      -1， 5， -1        0  -1
 1，    1， 1      0， -1， 0

 OpenCV自定义滤波器API:
 void cv::filter2D(
 InputArray src,
 OutputArray dst,
 int ddepth, // 默认-1
 InputArray kernel, // 卷积核或者卷积窗口大小
 Point anchor = Point(-1,-1),
 double delta = 0,
 int borderType = BORDER_DEFAULT
 )
 int ddepth, // 默认-1，表示输入与输出图像类型一致，但是当涉及浮点数计算时候，需要设置为CV_32F。
 滤波完成之后需要使用convertScaleAbs函数将结果转换为字节（uchar）类型。
 
 void cv::convertScaleAbs    (    InputArray     src,
 OutputArray     dst,
 double     alpha = 1,
 double     beta = 0
 )
 \texttt{dst} (I)= \texttt{saturate\_cast<uchar>} (| \texttt{src} (I)* \texttt{alpha} + \texttt{beta} |)
 convertScaleAbs函数为 abs(src*alpha+beta) 再通过saturate_cast函数转换到0-255
 缩放，计算绝对值，然后将结果转换为8位。
 */
namespace Day030 {
    void mainFunction(){
        Mat src = imread("./data/images/lena.jpg");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        
        imshow("input", src);

        // 均值模糊卷积核
        Mat kernel1 = Mat::ones(5, 5, CV_32F) / (float)(25);
        
        // 锐化
        Mat kernel2 = (Mat_<char>(3, 3) << 0, -1, 0,
            -1, 5, -1,
            0, -1, 0);

        // 梯度边缘
        Mat kernel3 = (Mat_<int>(2, 2) << 1, 0, 0, -1);

        Mat dst1, dst2, dst3;
        filter2D(src, dst1, -1, kernel1);
        filter2D(src, dst2, -1, kernel2);
        filter2D(src, dst3, CV_32F, kernel3);
        convertScaleAbs(dst3, dst3); // 缩放，计算绝对值，然后将结果转换为8位。 

        imshow("blur 5x5", dst1);
        imshow("sharpen 3x3", dst2);
        imshow("gradient 2x2", dst3);

        waitKey(0);
    }
}
