//
//  day021.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/10.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day021-图像卷积操作
 图像卷积可以看成是一个窗口区域在另外一个大的图像上移动，对每个窗口覆盖的区域都进行点乘得到的值作为中心像素点的输出值。
 窗口的移动是从左到右，从上到下。窗口可以理解成一个指定大小的二维矩阵，里面有预先指定的值。

 相关API
     - blur(
     InputArray     src, // 输入
     OutputArray     dst, 输出
     Size     ksize, // 窗口大小
     Point     anchor = Point(-1,-1), // 默认值
     int     borderType = BORDER_DEFAULT // 默认值
     )
     卷积核所有值为1/(ksize.width*ksize.height)
     官方文档：https://docs.opencv.org/master/d4/d86/group__imgproc__filter.html#ga8c45db9afe636703801b0b2e440fce37
 */
namespace Day021 {
    void mainFunction(){
        Mat src = imread("./data/images/lena.jpg");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        Mat dst;
        blur(src, dst, Size(3, 3));
        
        Mat custom_dst = custom_3x3_blur(src);
        
        imshow("src", src);
        imshow("custom_dst", custom_dst);
        imshow("dst", custom_dst);
        waitKey(0);
    }
    Mat custom_3x3_blur(Mat src){
        int h = src.rows;
        int w = src.cols;

        Mat dst = src.clone();
        for (int row = 1; row < h-1; row++) {
            for (int col = 1; col < w-1; col++) {
                Vec3b p1 = src.at<Vec3b>(row-1, col-1);
                Vec3b p2 = src.at<Vec3b>(row-1, col);
                Vec3b p3 = src.at<Vec3b>(row-1, col+1);
                Vec3b p4 = src.at<Vec3b>(row, col-1);
                Vec3b p5 = src.at<Vec3b>(row, col);
                Vec3b p6 = src.at<Vec3b>(row, col+1);
                Vec3b p7 = src.at<Vec3b>(row+1, col-1);
                Vec3b p8 = src.at<Vec3b>(row+1, col);
                Vec3b p9 = src.at<Vec3b>(row+1, col+1);

                int b = p1[0] + p2[0] + p3[0] + p4[0] + p5[0] + p6[0] + p7[0] + p8[0] + p9[0];
                int g = p1[1] + p2[1] + p3[1] + p4[1] + p5[1] + p6[1] + p7[1] + p8[1] + p9[1];
                int r = p1[2] + p2[2] + p3[2] + p4[2] + p5[2] + p6[2] + p7[2] + p8[2] + p9[2];

                dst.at<Vec3b>(row, col)[0] = saturate_cast<uchar>(b / 9);
                dst.at<Vec3b>(row, col)[1] = saturate_cast<uchar>(g / 9);
                dst.at<Vec3b>(row, col)[2] = saturate_cast<uchar>(r / 9);
            }
        }
        return dst;
    }
}
