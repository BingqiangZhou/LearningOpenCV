//
//  day006.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/1/31.
//

#include <stdio.h>

#include <string>

#include "toc.h"

using namespace cv;

/* Day006-LUT(Look Up Table, 查找表)的作用与用法
 applyColorMap(src, dst, COLORMAP)
     - src 表示输入图像
     - dst表示输出图像
     - 匹配到的颜色LUT， OpenCV支持13种颜色风格的查找表映射
 主要用途：颜色匹配、伪色彩增强
 支持以下22种colormap：
     01. COLORMAP_AUTUMN
     02. COLORMAP_BONE
     03. COLORMAP_JET
     04. COLORMAP_WINTER
     05. COLORMAP_RAINBOW
     06. COLORMAP_OCEAN
     07. COLORMAP_SUMMER
     08. COLORMAP_SPRING
     09. COLORMAP_COOL
     10. COLORMAP_HSV
     11. COLORMAP_PINK
     12. COLORMAP_HOT
     13. COLORMAP_PARULA
     14. COLORMAP_MAGMA
     15. COLORMAP_INFERNO
     16. COLORMAP_PLASMA
     17. COLORMAP_VIRIDIS
     18. COLORMAP_CIVIDIS
     19. COLORMAP_TWILIGHT
     20. COLORMAP_TWILIGHT_SHIFTED
     21. COLORMAP_TURBO
     22. COLORMAP_DEEPGREEN
 参考链接：https://docs.opencv.org/master/d3/d50/group__imgproc__colormap.html#ga9a805d8262bcbe273f16be9ea2055a65
 22种颜色效果可查看：https://cloud.tencent.com/developer/article/1582400
 */
namespace Day006 {
    void mainFunction(){
        Mat src = imread("./data/images/canjian.jpg");
//        Mat src = imread("./data/images/cos.jpg");
        imshow("source image", src);
        
        for (int i = 0; i < 22; i++) {
            Mat new_src;
            applyColorMap(src, new_src, i);
            imshow("image: " + std::to_string(i), new_src);
        }
        
        Mat gray;
        cvtColor(src, gray, COLOR_BGR2GRAY);
        customColorMap(gray);
        imshow("custom colormap", gray);
        waitKey(0);
    };
    // 自定义colormap，颜色值小于127的对应0，颜色值大于127的对应255。
    void customColorMap(cv::Mat &image){
        int lut[256];
        for (int i = 0; i < 256; i++) {
            if (i < 127) {
                lut[i] = 0;
            }else{
                lut[i] = 255;
            }
        }
        
        int h = image.rows;
        int w = image.cols;
        for (int row = 0; row < h; row++) {
            for (int col = 0; col < w; col++) {
                int v = image.at<uchar>(row, col);
                image.at<uchar>(row, col) = lut[v];
            }
        }
    }
}
