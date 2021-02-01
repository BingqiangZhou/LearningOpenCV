//
//  day013.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/2.
//

#include <stdio.h>

#include "toc.h"

using namespace cv;

/** Day013-图像翻转(Image Flip)
 图像翻转的本质像素映射，OpenCV支持三种图像翻转方式
 - X轴翻转，flipcode = 0
 - Y轴翻转, flipcode = 1
 - XY轴翻转, flipcode = -1

 相关的API
 flip
 - src输入参数
 - dst 翻转后图像
 - flipcode
 */
namespace Day013 {
    void mainFunction(){
        Mat src = imread("./data/images/cos.jpg");
        imshow("source image", src);

        Mat dst;
        
        // 上下翻转 x flip
        flip(src, dst, 0);
        imshow("X flip", dst);

        // 左右翻转 y flip
        flip(src, dst, 1);
        imshow("Y flip", dst);

        // 上下左右同时翻转 x y flip
        flip(src, dst, -1);
        imshow("XY flip", dst);

        int height = src.rows;
        int width = src.cols;
        int c = src.channels();
        
        Mat temp = Mat::zeros(src.size(), src.type());
        
        // 自行实现 上下翻转
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                if (c == 3) {
                    temp.at<Vec3b>(row, col) = src.at<Vec3b>(height - row - 1, col);
                }
            }
        }
        imshow("custom x flip", temp);

        // 自行实现 水平翻转
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                if (c == 3) {
                    temp.at<Vec3b>(row, col) = src.at<Vec3b>(row, width - col - 1);
                }
            }
        }
        imshow("custom y flip", temp);


        // 自行实现 上下左右同时翻转
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                if (c == 3) {
                    temp.at<Vec3b>(row, col) = src.at<Vec3b>(height - row - 1, width - col - 1);
                }
            }
        }
        imshow("custom xy flip", temp);

        waitKey(0);
    }
}
