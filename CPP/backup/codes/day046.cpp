//
//  day046.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/17.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day046-二值图像联通组件寻找
 连通组件标记算法介绍
 连接组件标记算法(connected component labeling algorithm)是图像分析中最常用的算法之一，
 算法的实质是扫描二值图像的每个像素点，对于像素值相同的而且相互连通分为相同的组(group)，最终得到图像中所有的像素连通组件。
 扫描的方式可以是从上到下，从左到右，对于一幅有N个像素的图像来说，最大连通组件个数为N/2。
 扫描是基于每个像素单位，OpenCV中进行连通组件扫码调用的时候必须保证背景像素是黑色、前景像素是白色。
 
 最常见的连通组件扫码有如下两类算法：
     1. 基于图的搜索算法（一步法）
     2. 基于扫描、等价类合并算法（两步法）

 OpenCV中支持连通组件扫描的API有两个，一个是带统计信息一个不带统计信息。
 不带统计信息的API及其解释如下：
 int cv::connectedComponents(
 InputArray     image, // 输入二值图像，黑色背景
 OutputArray     labels, // 输出的标记图像，背景index=0
 int     connectivity = 8, // 连通域，默认是8连通
 int     ltype = CV_32S // 输出的labels类型，默认是CV_32S
 )
 */
namespace Day046 {
    void mainFunction(){
        Mat src = imread("./data/images/rice.png");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        imshow("original", src);
        
        Mat blured, gray, binary, labels, colored_labels;
        
        GaussianBlur(src, blured, Size(3, 3), 0); // 高斯模糊
        cvtColor(blured, gray, COLOR_BGR2GRAY); // 转换为灰度图
        double thresh = threshold(gray, binary, 0, 255, THRESH_OTSU); // 转换为二值图
        cout << "OTSU threshold: " << thresh << endl;
        imshow("THRESH_OTSU", binary);
        
        int nums_labels = connectedComponents(binary, labels, 8, CV_32S); // 二值图像联通组件寻找
        cout << "the number of rice: " << nums_labels - 1 << endl;
        
        // 将不同的label应用不同的颜色
        Mat temp = Mat::zeros(labels.size(), CV_32S);
        normalize(labels, temp, 0, 255, NORM_MINMAX);
        temp.convertTo(labels, CV_8U);
        applyColorMap(labels, colored_labels, COLORMAP_HOT);
        imshow("colored_labels", colored_labels);
        
        waitKey(0);
        destroyAllWindows();
    }
}
