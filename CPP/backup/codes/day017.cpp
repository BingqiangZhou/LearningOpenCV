//
//  day017.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/8.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day017-图像直方图
 图像直方图的解释
 图像直方图是图像像素值的统计学特征、计算代价较小，具有图像平移、旋转、缩放不变性等众多优点，
 广泛地应用于图像处理的各个领域，特别是灰度图像的阈值分割、基于颜色的图像检索以及图像分类、反向投影跟踪。
 常见的分为灰度直方图、颜色直方图

 Bins是指直方图的大小范围， 对于像素值取值在0～255之间的，最少有256个bin，此外还可以有16、32、48、128等，256除以bin的大小应该是整数倍。

 OpenCV中相关API
 calcHist(const Mat *images,int nimages,const int *channels,InputArray mask,OutputArray hist,
             int dims,const int *histSize, const float **ranges,bool uniform = true,bool accumulate = false)
 calcHist(const Mat *images,int nimages,const int *channels, InputArray mask,SparseMat &hist,
            int dims,const int *histSize,const float **ranges,bool uniform = true,bool accumulate = false)
 calcHist(InputArrayOfArrays images,const std::vector< int > &channels,InputArray mask,OutputArray hist,
            const std::vector< int > &histSize,const std::vector< float > &ranges,bool accumulate = false)
 */
namespace Day017 {
    void mainFunction(){
        Mat src = imread("./data/images/cos.jpg");
        imshow("source image", src);
        
        // 注意严格保证类型正确
        Mat b_hist, g_hist, r_hist;
        vector<Mat> bgr;
        split(src, bgr);
        const int bins[] = {256};
        float range[] = {0, 255};
        const float* ranges[] = {range};
        
        // 计算直方图
        calcHist(&bgr[0], 1, 0, Mat(), b_hist, 1, bins, ranges);
        calcHist(&bgr[1], 1, 0, Mat(), g_hist, 1, bins, ranges);
        calcHist(&bgr[2], 1, 0, Mat(), r_hist, 1, bins, ranges);
        
        showHist(b_hist, "b");
        showHist(g_hist, "g");
        showHist(r_hist, "r");
        
        vector<Mat> bgr_hist = {b_hist, g_hist, r_hist};
        showHist(bgr_hist, "bgr");
        
        waitKey(0);
        destroyAllWindows();
    }
    void showHist(Mat hist, string title){
        int hist_w = 512;
        int hist_h = 400;
        Mat histImage = Mat::zeros(hist_h, hist_w, CV_8UC3);
        
        int bins = hist.rows;
        int bin_w = cvRound((double)hist_w / bins);
        
        normalize(hist, hist, 0, histImage.rows, NORM_MINMAX, -1, Mat());
        
        for (int i = 1; i < bins; i++) {
            line(histImage, Point(bin_w*(i - 1), hist_h - cvRound(hist.at<float>(i - 1))),
                Point(bin_w*(i), hist_h - cvRound(hist.at<float>(i))),Scalar(0, 0, 255), 2, 8, 0);
        }
        
        imshow(title, histImage);
    }

    void showHist(vector<Mat> hist_list, string title){
        int hist_w = 512;
        int hist_h = 400;
        Mat histImage = Mat::zeros(hist_h, hist_w, CV_8UC3);
        vector<Scalar> colors = {Scalar(255, 0, 0), Scalar(0, 255, 0), Scalar(0, 0, 255)};
        
        int index = 0;
        for (Mat hist : hist_list) {
            int bins = hist.rows;
            int bin_w = cvRound((double)hist_w / bins);
            
            
            normalize(hist, hist, 0, histImage.rows, NORM_MINMAX, -1, Mat());
            
            for (int i = 1; i < bins; i++) {
                line(histImage, Point(bin_w*(i - 1), hist_h - cvRound(hist.at<float>(i - 1))),
                    Point(bin_w*(i), hist_h - cvRound(hist.at<float>(i))), colors[index], 2, 8, 0);
            }
            index++;
        }
        
        imshow(title, histImage);
    }
}
