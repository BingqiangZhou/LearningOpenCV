//
//  day041.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/17.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day041-OpenCV中的基本阈值操作
 假设我们已经寻找到合适的阈值T，那么对图像二值化分割可以看成是一种基本的阈值化操作，
 其实OpenCV除了支持正常的二值化阈值分割操作之外，还支持一些其它的阈值操作，OpenCV中支持的阈值操作的API如下：
     double cv::threshold(
     InputArray src,
     OutputArray dst,
     double thresh,
     double maxval,
     int type
     )
 其中type表示阈值分割的方法，支持如下五种：
     THRESH_BINARY = 0       二值分割，如果值大于thresh，则为maxval否则为0
     THRESH_BINARY_INV = 1   反向二值分割，如果值大于thresh，则为0否则为maxval
     THRESH_TRUNC = 2        截断，如果值大于thresh，则为thresh，否则为原来的值
     THRESH_TOZERO = 3       取零，如果值大于thresh，则为原来的值，否则为0
     THRESH_TOZERO_INV = 4   反向取零，如果值大于thresh，则为0，否则为原来的值
 阈值分割方法参考：
         https://docs.opencv.org/master/d7/d1b/group__imgproc__misc.html#gaa9e58d2860d4afa658ef70a9b1115576
 */
namespace Day041 {
    void mainFunction(){
        Mat src = imread("./data/images/lena.jpg");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        cvtColor(src, src, COLOR_BGR2GRAY);
        imshow("original", src);

        int methods[] = {THRESH_BINARY, THRESH_BINARY_INV, THRESH_TRUNC, THRESH_TOZERO, THRESH_TOZERO_INV};
        string method_names[] = {"THRESH_BINARY", "THRESH_BINARY_INV", "THRESH_TRUNC", "THRESH_TOZERO", "THRESH_TOZERO_INV"};
        
        Mat binary;
        int t = 127, i = 0;
        for (int method : methods) {
            threshold(src, binary, t, 255, method);
            imshow(method_names[i], binary);
            i++;
        }
        
        waitKey(0);
    }
}
