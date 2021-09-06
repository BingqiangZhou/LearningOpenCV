//
//  day028.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/14.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day028-图像积分图算法
 积分图像是Crow在1984年首次提出，是为了在多尺度透视投影中提高渲染速度，是一种快速计算图像区域和与平方和的算法。
 其核心思想是对每个图像建立自己的积分图查找表，在图像积分处理计算阶段根据预先建立的积分图查找表，
 直接查找从而实现对均值卷积线性时间计算，做到了卷积执行的时间与半径窗口大小的无关联。
 图像积分图在图像特征提取HAAR/SURF、二值图像分析、图像相似相关性NCC计算、图像卷积快速计算等方面均有应用，是图像处理中的经典算法之一。

 图像积分图建立与查找
 在积分图像(Integral Image - ii)上任意位置(x, y)处的ii(x, y)表示该点左上角所有像素之和， 其中(x,y)是图像像素点坐标。
 
 OpenCV中的相关API如下：
 integral(
 InputArray src, // 输入图像
 OutputArray sum, // 和表
 OutputArray sqsum, // 平方和表
 OutputArray tilted, // 瓦块和表
 int sdepth = -1, // 和表数据深度常见CV_32S
 int sqdepth = -1 // 平方和表数据深度 常见 CV_32F
 )
 官方文档：integral - https://docs.opencv.org/master/d7/d1b/group__imgproc__misc.html#ga97b87bec26908237e8ba0f6e96d23e28
 */
namespace Day028 {
    void mainFunction(){
        Mat src = imread("./data/images/example.png");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        imshow("input", src);

        Mat dst;
        Mat sum, sqrsum;
        integral(src, sum, sqrsum, CV_32S, CV_32F); // 计算和(sum)表、平方和表(sqsum)表
        dst = blur_demo(src, sum);
        imshow("result", dst);

        waitKey(0);
    }
    // 通过和(sum)表来计算均值模糊
    Mat blur_demo(Mat &image, Mat &sum) {
        int w = image.cols;
        int h = image.rows;
        Mat result = Mat::zeros(image.size(), image.type());
        int x2 = 0, y2 = 0;
        int x1 = 0, y1 = 0;
        int ksize = 5;
        int radius = ksize / 2;
        int ch = image.channels();
        int cx = 0, cy = 0;
        for (int row = 0; row < h + radius; row++) {
            // 计算左上角（y1）与右下角（y2）的y坐标
            y2 = (row + 1)>h ? h : (row + 1);
            y1 = (row - ksize) < 0 ? 0 : (row - ksize);
            for (int col = 0; col < w + radius; col++) {
                // 计算左上角（x1）与右下角（x2）的x坐标
                x2 = (col + 1)>w ? w : (col + 1);
                x1 = (col - ksize) < 0 ? 0 : (col - ksize);
                // 计算卷积中心位置
                cx = (col - radius) < 0 ? 0 : col - radius;
                cy = (row - radius) < 0 ? 0 : row - radius;
                // 计算卷积框区域的大小（面积，高乘宽）
                int num = (x2 - x1)*(y2 - y1);
                for (int i = 0; i < ch; i++) {
                    // 获取卷积框区域内像素值的和
                    int s = getblockSum(sum, x1, y1, x2, y2, i);
                    // 卷积框区域内像素值的和除以面积则为平均值
                    result.at<Vec3b>(cy, cx)[i] = saturate_cast<uchar>(s / num);
                }
            }
        }
        return result;
    }
    // 根据和（sum）表计算卷积框内的像素值的和
    int getblockSum(Mat &sum, int x1, int y1, int x2, int y2, int i) {
        int tl = sum.at<Vec3i>(y1, x1)[i];
        int tr = sum.at<Vec3i>(y2, x1)[i];
        int bl = sum.at<Vec3i>(y1, x2)[i];
        int br = sum.at<Vec3i>(y2, x2)[i];
        int s = (br - bl - tr + tl);
        return s;
    }
}
