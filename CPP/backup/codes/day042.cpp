//
//  day042.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/17.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day042-OpenCV中图像二值寻找算法 – OTSU
 图像二值化，除了我们上次分享的手动阈值设置与根据灰度图像均值的方法之外，
 还有几个根据图像直方图实现自动全局阈值寻找的方法，OpenCV中支持的有OTSU与Triangle两种直方图阈值寻找算法。
 其中OTSU的是通过计算类间最大方差来确定分割阈值的阈值选择算法，
 OTSU算法对直方图有两个峰，中间有明显波谷的直方图对应图像二值化效果比较好，
 而对于只有一个单峰的直方图对应的图像分割效果没有双峰的好。

 OpenCV中OTSU算法使用只需要在threshold函数的type类型声明THRESH_OTSU即可。
 */
namespace Day042 {
    void mainFunction(){
        Mat src = imread("./data/images/lena.jpg");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        cvtColor(src, src, COLOR_BGR2GRAY);
        imshow("original", src);

        Mat binary;
        double thresh = threshold(src, binary, 0, 255, THRESH_OTSU);
        cout << "threshold: " << thresh << endl;
        imshow("THRESH_OTSU", binary);
        
        waitKey(0);

    }
}
