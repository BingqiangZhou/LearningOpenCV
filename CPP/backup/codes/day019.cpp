//
//  day019.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/9.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day019-图像直方图比较
 图像直方图比较，就是计算两幅图像的直方图数据，比较两组数据的相似性，从而得到两幅图像之间的相似程度，
 直方图比较在早期的CBIR(Content-based image retrieval, 基于内容的图像检索 )中是应用很常见的技术手段，
 通常会结合边缘处理、词袋等技术一起使用。

 OpenCV中直方图比较的API很简单
 compareHist(hist1, hist2, method)
     -常见比较方法有
         相关性：越接近+1越相似，越不相似越接近-1
         卡方： 值越小越相似
         交叉：不太准
         巴氏距离：越接近0则越相似
     具体公式可见：HistCompMethods，https://docs.opencv.org/master/d6/dc7/group__imgproc__hist.html#ga994f53817d621e2e4228fc646342d386
 */
namespace Day019 {
    void mainFunction(){
        Mat src1 = imread("./data/images/m1.png");
        Mat src2 = imread("./data/images/m2.png");
        Mat src3 = imread("./data/images/cos.jpg");
        Mat src4 = imread("./data/images/test.png");

        // 可视化图像
        imshow("src1", src1);
        imshow("src2", src2);
        imshow("src3", src3);
        imshow("src4", src4);

        // bgr to hsv,在图像处理中，常常转到HSV色彩空间，并且最常用的通道就是H、S分量
        Mat hsv1, hsv2, hsv3, hsv4;
        cvtColor(src1, hsv1, COLOR_BGR2HSV);
        cvtColor(src2, hsv2, COLOR_BGR2HSV);
        cvtColor(src3, hsv3, COLOR_BGR2HSV);
        cvtColor(src4, hsv4, COLOR_BGR2HSV);

        // 计算H、S通道的直方图，H（0～180）、S（0-256）
        int h_bins = 60; int s_bins = 64;
        int histSize[] = { h_bins, s_bins };
        float h_ranges[] = { 0, 180 };
        float s_ranges[] = { 0, 256 };
        const float* ranges[] = { h_ranges, s_ranges };
        int channels[] = { 0, 1 };
        Mat hist1, hist2, hist3, hist4;
        calcHist(&hsv1, 1, channels, Mat(), hist1, 2, histSize, ranges, true, false);
        calcHist(&hsv2, 1, channels, Mat(), hist2, 2, histSize, ranges, true, false);
        calcHist(&hsv3, 1, channels, Mat(), hist3, 2, histSize, ranges, true, false);
        calcHist(&hsv4, 1, channels, Mat(), hist4, 2, histSize, ranges, true, false);
        
        // 数值归一化，注意确保输入是浮点类型
        normalize(hist1, hist1, 0, 1, NORM_MINMAX, -1, Mat());
        normalize(hist2, hist2, 0, 1, NORM_MINMAX, -1, Mat());
        normalize(hist3, hist3, 0, 1, NORM_MINMAX, -1, Mat());
        normalize(hist4, hist4, 0, 1, NORM_MINMAX, -1, Mat());
        
        // 直方图比较
        unordered_map<string, int> methods_dict = {
            {"Correlation", HISTCMP_CORREL},                   // 相关性
            {"Chi-Square", HISTCMP_CHISQR},                    // 卡方
            {"Intersection", HISTCMP_INTERSECT},               // 交叉
            {"Bhattacharyya distance", HISTCMP_BHATTACHARYYA}  // 巴式距离
        };
        
        for (pair<string, int> method: methods_dict) {
            double v1 = compareHist(hist1, hist2, method.second);
            double v2 = compareHist(hist3, hist4, method.second);
            cout << method.first << endl;
            cout << "v1: " << v1 << ", v2: " << v2 << endl;
        }

        waitKey(0);
    }
}
