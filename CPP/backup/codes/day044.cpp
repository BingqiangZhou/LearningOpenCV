//
//  day044.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/17.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day044-OpenCV中图像二化自适应阈值算法
 OpenCV中的自适应阈值算法主要是基于均值实现，
 根据计算均值的方法不同分为盒子模糊均值与高斯模糊均值，
 然后使用原图减去均值图像，得到的差值图像进行自适应分割，
 相关的API如下：
     void cv::adaptiveThreshold(
     InputArray src,
     OutputArray dst,
     double maxValue,
     int adaptiveMethod,
     int thresholdType,
     int blockSize,
     double C
     )
 其中blockSize取值必须是奇数，C取值在10左右

 自适应方法类型：
 ADAPTIVE_THRESH_GAUSSIAN_C = 1
 ADAPTIVE_THRESH_MEAN_C = 0

 当阈值操作类型thresholdType为：THRESH_BINARY
 二值图像 = 原图 – 均值图像 > -C ? 255 : 0

 当阈值操作类型thresholdType为：THRESH_BINARY_INV
 二值图像 = 原图 – 均值图像 > -C ? 0 : 255
 */
namespace Day044 {
    void mainFunction(){
        Mat src = imread("./data/images/text1.png");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        cvtColor(src, src, COLOR_BGR2GRAY);
        imshow("original", src);

        Mat binary_THRESH_TRIANGLE, binary_THRESH_OTSU,
            binary_ADAPTIVE_THRESH_GAUSSIAN_C, binary_ADAPTIVE_THRESH_MEAN_C;
        
        // TRIANGLE
        double thresh = threshold(src, binary_THRESH_TRIANGLE, 0, 255, THRESH_TRIANGLE);
        cout << "THRESH_TRIANGLE threshold: " << thresh << endl;
        imshow("THRESH_TRIANGLE", binary_THRESH_TRIANGLE);
        
        // OTSU
        thresh = threshold(src, binary_THRESH_OTSU, 0, 255, THRESH_OTSU);
        cout << "THRESH_OTSU threshold: " << thresh << endl;
        imshow("THRESH_OTSU", binary_THRESH_TRIANGLE);
        
        // ADAPTIVE_THRESH_GAUSSIAN_C
        adaptiveThreshold(src, binary_ADAPTIVE_THRESH_GAUSSIAN_C, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY, 25, 10);
        imshow("ADAPTIVE_THRESH_GAUSSIAN_C", binary_ADAPTIVE_THRESH_GAUSSIAN_C);
        
        // ADAPTIVE_THRESH_MEAN_C
        adaptiveThreshold(src, binary_ADAPTIVE_THRESH_MEAN_C, 255, ADAPTIVE_THRESH_MEAN_C, THRESH_BINARY, 25, 10);
        imshow("ADAPTIVE_THRESH_MEAN_C", binary_ADAPTIVE_THRESH_MEAN_C);
        
        waitKey(0);
    }
}
