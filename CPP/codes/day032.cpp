//
//  day032.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/15.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day032-图像梯度 – 更多梯度算子
 图像的一阶导数算子除了sobel算子之外，常见的还有robert算子与prewitt算子，
 它们也都是非常好的可以检测图像的梯度边缘信息，通过OpenCV中自定义滤波器，
 使用自定义创建的robert与prewitt算子就可以实现图像的rober与prewitt梯度边缘检测，

 robert算子X方向  Y方向
     -1 0        0 -1
     0 1         1  0

 prewitt算子X方向  Y方向
 -1 -1 -1        -1 0 +1
  0  0  0        -1 0 +1
 +1 +1 +1        -1 0 +1

 OpenCV中的自定义算子滤波函数如下：

 filter2D(
 InputArray src,
 OutputArray dst,
 int ddepth,
 InputArray     kernel,
 Point anchor = Point(-1,-1),
 double delta = 0,
 int borderType = BORDER_DEFAULT
 )

 参考：
     https://blog.csdn.net/zaishuiyifangxym/article/details/89840396
     https://blog.csdn.net/swj110119/article/details/51777422
 */
namespace Day032 {
    void mainFunction(){
        Mat src = imread("./data/images/lena.jpg");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        imshow("input", src);

        Mat robert_x = (Mat_<int>(2, 2) << -1, 0, 0, 1);
        Mat robert_y = (Mat_<int>(2, 2) << 0, -1, 1, 0);

        Mat prewitt_x = (Mat_<char>(3, 3) << -1, 0, 1,
            -1, 0, 1,
            -1, 0, 1);
        Mat prewitt_y = (Mat_<char>(3, 3) << -1, -1, -1,
            0, 0, 0,
            1, 1, 1);

        Mat robert_grad_x, robert_grad_y, prewitt_grad_x, prewitt_grad_y;
        filter2D(src, robert_grad_x, CV_16S, robert_x);
        filter2D(src, robert_grad_y, CV_16S, robert_y);
        convertScaleAbs(robert_grad_x, robert_grad_x);
        convertScaleAbs(robert_grad_y, robert_grad_y);

        filter2D(src, prewitt_grad_x, CV_32F, prewitt_x);
        filter2D(src, prewitt_grad_y, CV_32F, prewitt_y);
        convertScaleAbs(prewitt_grad_x, prewitt_grad_x);
        convertScaleAbs(prewitt_grad_y, prewitt_grad_y);
        printf("image gradient...\n");

        imshow("robert x", robert_grad_x);
        imshow("robert y", robert_grad_y);
        imshow("prewitt x", prewitt_grad_x);
        imshow("prewitt y", prewitt_grad_y);

        waitKey(0);
    }
}
