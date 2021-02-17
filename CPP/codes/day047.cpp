//
//  day047.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/17.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day047-二值图像连通组件状态统计
 OpenCV中的连通组件标记算法有两个相关的API，
 一个是不带统计信息的API
     int cv::connectedComponents(
     InputArray     image, // 输入二值图像，黑色背景
     OutputArray     labels, // 输出的标记图像，背景index=0
     int     connectivity = 8, // 连通域，默认是8连通
     int     ltype = CV_32S // 输出的labels类型，默认是CV_32S
     )
 另外一个是会输出连通组件统计信息的相关API，
     int cv::connectedComponentsWithStats(
     InputArray image,
     OutputArray labels,
     OutputArray stats,
     OutputArray centroids,
     int connectivity,
     int ltype,
     int ccltype
     )
 相关的统计信息包括在输出stats的对象中，每个连通组件有一个这样的输出结构体。
 CC_STAT_LEFT 连通组件外接矩形左上角坐标的X位置信息

 CC_STAT_TOP 连通组件外接左上角坐标的Y位置信息

 CC_STAT_WIDTH 连通组件外接矩形宽度

 CC_STAT_HEIGHT 连通组件外接矩形高度

 CC_STAT_AREA 连通组件的面积大小，基于像素多少统计

 Centroids输出的是每个连通组件的中心位置坐标(x, y)
 */
namespace Day047 {
    void mainFunction(){
        Mat src = imread("./data/images/rice.png");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        // imshow("original", src);
        
        Mat blured, gray, binary, labels, stats, centroids, colored_labels;
        
        GaussianBlur(src, blured, Size(3, 3), 0); // 高斯模糊
        cvtColor(blured, gray, COLOR_BGR2GRAY); // 转换为灰度图
        double thresh = threshold(gray, binary, 0, 255, THRESH_OTSU); // 转换为二值图
        cout << "OTSU threshold: " << thresh << endl;
        // imshow("THRESH_OTSU", binary);
        
        // int nums_labels = connectedComponents(binary, labels, 8, CV_32S); // 二值图像联通组件寻找
        int nums_labels = connectedComponentsWithStats(binary, labels, stats, centroids);// 带状态的二值图像联通组件寻找
        cout << "the number of rice: " << nums_labels - 1 << endl;
        
        // 在图像中画出联通组件的中心以及外接矩形框
        int x, y, w, h, s, cx, cy;
        for (int i = 0; i < nums_labels; i++) {
            if (i == 0) { // 跳过背景
                continue;
            }
            x = stats.at<int>(i, CC_STAT_LEFT);     // 左上角x坐标
            y = stats.at<int>(i, CC_STAT_TOP);      // 左上角y坐标
            w = stats.at<int>(i, CC_STAT_WIDTH);    // 宽
            h = stats.at<int>(i, CC_STAT_HEIGHT);   // 高
            s = stats.at<int>(i, CC_STAT_AREA);     // 面积
            
            rectangle(src, Point(x, y), Point(x + w, y + h), Scalar(0, 0, 255));
            
            cx = centroids.at<double>(i, 0);        // 中心点x坐标
            cy = centroids.at<double>(i, 1);        // 中心点y坐标
            
            circle(src, Point(cx, cy), 4, Scalar(0, 0, 255), FILLED);
        }
        imshow("original", src);
        
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

