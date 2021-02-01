//
//  day010.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/1.
//

#include <stdio.h>

#include "toc.h"

using namespace cv;


/* Day010-图像像素值统计
 像素值统计
 - 最小(min)
 - 最大(max)
 - 均值(mean)
 - 标准方差(standard deviation)

 API
 - 最大最小值minMaxLoc
 - 计算均值与标准方差meanStdDev
 */
namespace Day010 {
    void mainFunction(){
//        Mat src = imread("./data/images/cos.jpg", IMREAD_GRAYSCALE);
        Mat src = imread("./data/images/cos.jpg");
        imshow("source image", src);
        
        // 最大最小值minMaxLoc
        
        // 需要注意的是，只能在单通道上操作
        Mat gray;
        cvtColor(src, gray, COLOR_BGR2GRAY);
        
        double min_val = 0, max_val = 0;
        Point min_loc, max_loc;
        minMaxLoc(gray, &min_val, &max_val, &min_loc, &max_loc);
        printf("minVal: %.2f, maxVal: %.2f\n", min_val, max_val);
        printf("minVal: x %d, y %d, maxVal: x %d, y %d\n", min_loc.x, min_loc.y, max_loc.x, max_loc.y);
        
        // 计算均值与标准方差meanStdDev
        Mat mean, stddev;
        meanStdDev(src, mean, stddev);
        printf("mean: (%.2f, %.2f, %.2f)\n", mean.at<double>(0, 0), mean.at<double>(1, 0), mean.at<double>(2, 0));
        printf("stddev: (%.2f, %.2f, %.2f)\n", stddev.at<double>(0, 0), stddev.at<double>(1, 0), stddev.at<double>(2, 0));
        
        Mat dst = Mat::zeros(src.size(), src.type());
        int h = src.rows;
        int w = src.cols;
        int c = src.channels();
        for (int row = 0; row < h; row++) {
            for (int col = 0; col < w; col++) {
                for (int k = 0; k < c; k++) {
                    // 如果当前通道的值大于当前通道的均值，则赋为255，否则为0（已初始化为0）
                    if (src.at<Vec3b>(row, col)[k] > mean.at<double>(k, 0)) {
                        dst.at<Vec3b>(row, col)[k] = 255;
                    }
                }
            }
        }
        imshow("dst", dst);
        
        waitKey(0);
    }
}
