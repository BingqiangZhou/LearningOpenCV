//
//  day020.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/10.
//

#include <stdio.h>

#include "toc.h"

using namespace cv;
using namespace std;

/**Day020-图像直方图反向投影
 文字解释：图像直方图反向投影是通过构建指定模板图像的二维直方图空间与目标的二维直方图空间，
 进行直方图数据归一化之后，进行比率操作，对所有得到非零数值，
 生成查找表对原图像进行像素映射之后，再进行图像模糊输出的结果。

 通俗来说就是
 给一个模版图像和一个目标图像，在目标图像中找模版图像的响应位置，再通过查找表映射输出一个表示响应值大小的图像
 最后适用卷积模糊降低反向投影之后图像结果的噪声

 直方图反向投影流程：
 - 计算直方图
 - 归一化输出
 - 计算比率R
 - LUT查找表
 - 卷积模糊

 相关API
 - calcBackProject(const Mat *images,int nimages,const int *channels,InputArray hist,OutputArray backProject,
                const float **ranges,double scale = 1,bool uniform = true)
 - calcBackProject(const Mat *images,int nimages,const int *channels,const SparseMat &hist,OutputArray backProject,
                const float **ranges,double scale = 1,bool uniform = true)
 - calcBackProject(InputArrayOfArrays images,const std::vector< int > &channels,InputArray hist,OutputArray dst,
                const std::vector< float > &ranges,double scale)
 */
namespace Day020 {
    void mainFunction(){
        Mat src = imread("./data/images/sample.png");
        Mat model = imread("./data/images/target.png");
        if (src.empty() || model.empty()) {
            cout  << "could not load image..." << endl;
            return ;
        }
        imshow("roi_image", src);
        imshow("target_model", model);

        backProject(src, model, true);
        waitKey(0);
    };
    void backProject(cv::Mat roi_image, cv::Mat target_model, bool show_fig){
        Mat target_hsv, roi_hsv;
        cvtColor(roi_image, roi_hsv, COLOR_BGR2HSV);
        cvtColor(target_model, target_hsv, COLOR_BGR2HSV);

        // 设置bins
        int h_bins = 32; int s_bins = 32;
        int histSize[] = { h_bins, s_bins };
        
        // hue varies from 0 to 179, saturation from 0 to 255
        float h_ranges[] = { 0, 180 };
        float s_ranges[] = { 0, 256 };
        const float* ranges[] = { h_ranges, s_ranges };
        int channels[] = { 0, 1 };
        
        // 计算直方图
        Mat roi_hist;
        calcHist(&roi_hsv, 1, channels, Mat(), roi_hist, 2, histSize, ranges, true, false);
        
        // normalize到[0, 255]
        normalize(roi_hist, roi_hist, 0, 255, NORM_MINMAX, -1, Mat());
        
        // 图像直方图反向映射
        MatND backproj;
        calcBackProject(&target_hsv, 1, channels, roi_hist, backproj, ranges, 1.0);
        
        if(show_fig == true){
            resize(roi_hist, roi_hist, Size(300, 300));
            imshow("roi_hist", roi_hist);
            imshow("BackProj", backproj);
        }
    }
}
