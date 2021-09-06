//
//  day043.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/17.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day043-OpenCV中图像二值寻找算法 – TRIANGLE
 图像二值化，除了我们上次分享的手动阈值设置与根据灰度图像均值的方法之外，
 还有几个根据图像直方图实现自动全局阈值寻找的方法，OpenCV中支持的有OTSU与Triangle两种直方图阈值寻找算法。
 上次分享提到OTSU基于类内最小方差实现阈值寻找, 它对有两个波峰之间有一个波谷的直方图特别好,
 但是有时候图像的直方图只有一个波峰,这个时候使用TRIANGLE方法寻找阈值是比较好的一个选择。

 OpenCV中TRIANGLE算法使用只需要在threshold函数的type类型声明THRESH_TRIANGLE即可。
 */
namespace Day043 {
    void mainFunction(){
        Mat src = imread("./data/images/lena.jpg");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        cvtColor(src, src, COLOR_BGR2GRAY);
        imshow("original", src);

        Mat binary;
        double thresh = threshold(src, binary, 0, 255, THRESH_TRIANGLE);
        cout << "threshold: " << thresh << endl;
        imshow("THRESH_TRIANGLE", binary);
        
        waitKey(0);

    }
}
