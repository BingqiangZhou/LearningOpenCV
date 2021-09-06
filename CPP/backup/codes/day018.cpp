//
//  day018.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/9.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day018-图像直方图均衡化
 图像直方图均衡化可以用于图像增强、对输入图像进行直方图均衡化处理，提升后续对象检测的准确率在OpenCV人脸检测的代码演示中已经很常见。
 此外对医学影像图像与卫星遥感图像也经常通过直方图均衡化来提升图像质量。

 OpenCV中直方图均衡化的API很简单
 - equalizeHist(src, dst)
 
 直方图均衡化原理可参考：
     https://zhuanlan.zhihu.com/p/44918476
     https://blog.csdn.net/qq_15971883/article/details/88699218 (有手算过程)
 */
namespace Day018 {
    void mainFunction(){
        Mat src = imread("./data/images/cos.jpg");

        if (src.empty()) {
            printf("could not load image...\n");
            return;
        }
        Mat gray, dst;
        cvtColor(src, gray, COLOR_BGR2GRAY);
        imshow("src", gray);
        equalizeHist(gray, dst);
        imshow("equalizeHist", dst);

        waitKey(0);
    }
}
