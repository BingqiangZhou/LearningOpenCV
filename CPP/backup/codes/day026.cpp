//
//  day026.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/14.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day026-边缘保留滤波算法 – 高斯双边模糊
 前面介绍的图像卷积处理无论是均值还是高斯都是属于模糊卷积，它们都有一个共同的特点就是模糊之后图像的边缘信息不复存在，受到了破坏。
 我们今天介绍的滤波方法有能力通过卷积处理实现图像模糊的同时对图像边缘不会造成破坏，滤波之后的输出完整的保存了图像整体边缘（轮廓）信息，
 我们称这类滤波算法为边缘保留滤波算法（EPF）。最常见的边缘保留滤波算法有以下几种
 -    高斯双边模糊
 -    Meanshift均值迁移模糊
 -    局部均方差模糊
 -    OpenCV中对边缘保留滤波还有一个专门的API
 高斯模糊是考虑图像空间位置对权重的影响，但是它没有考虑图像像素分布对图像卷积输出的影响，
 双边模糊考虑了像素值分布的影响，对像素值空间分布差异较大的进行保留从而完整的保留了图像的边缘信息。
 
 dst    = cv.bilateralFilter(src, d, sigmaColor, sigmaSpace[, dst[, borderType]])
 
 相关资料：https://blog.csdn.net/qq_41498261/article/details/101618119
 */
namespace Day026 {
    void mainFunction(){
        Mat src = imread("./data/images/example.png");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        
        imshow("input", src);

        Mat dst;
        bilateralFilter(src, dst, 0, 100, 10, 4);
        imshow("result", dst);

        waitKey(0);
    }
}
