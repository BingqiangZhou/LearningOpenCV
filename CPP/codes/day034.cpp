//
//  day034.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/15.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day034-图像锐化
 图像卷积的主要有三功能分别是图像的模糊/去噪、图像梯度/边缘发现、图像锐化/增强，
 前面的两个功能我们以前通过相关知识点的分享加以了解，学习了相关API的使用。
 图像锐化的本质是图像拉普拉斯滤波加原图权重像素叠加的输出 ：

 -1   -1  -1
 -1    C  -1
 -1    -1 -1
 
 当C值大于8时候表示图像锐化、越接近8表示锐化效果越好
 当C值等于8时候图像的高通滤波
 当C值越大，图像锐化效果在减弱、中心像素的作用在提升
 */
namespace Day034 {
    void mainFunction(){
        Mat src = imread("./data/images/lena.jpg");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        imshow("input", src);

        // 拉普拉斯算子(八邻域)
        // 1, 1, 1
        // 1, -8, 1
        // 1, 1, 1
        
        // 锐化算子
        Mat sharpen_kernel_8 = (Mat_<char>(3, 3) << -1, -1, -1,
                                                    -1, 9, -1,
                                                    -1, -1, -1);
        
        // 拉普拉斯算子(四邻域)
        // 0, 1, 0
        // 1, -4, 1
        // 0, 1, 0

        // 锐化算子
        Mat sharpen_kernel_4 = (Mat_<char>(3, 3) << 0, -1, 0,
                                                    -1, 5, -1,
                                                    0, -1, 0);

        Mat dst_sharpen_8, dst_sharpen_4;
        filter2D(src, dst_sharpen_8, CV_32F, sharpen_kernel_8);
        filter2D(src, dst_sharpen_4, CV_32F, sharpen_kernel_4);
        convertScaleAbs(dst_sharpen_8, dst_sharpen_8);
        convertScaleAbs(dst_sharpen_4, dst_sharpen_4);

        imshow("dst_sharpen_4", dst_sharpen_4);
        imshow("dst_sharpen_8", dst_sharpen_8);
        
        waitKey(0);
    }
}
