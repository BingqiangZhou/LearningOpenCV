//
//  day027.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/14.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day027-边缘保留滤波算法 – 均值迁移模糊(mean-shift blur)
 均值迁移模糊是图像边缘保留滤波算法中一种，经常用来在对图像进行分水岭分割之前去噪声，可以大幅度提升分水岭分割的效果。
 均值迁移模糊的主要思想如下：
     在图像进行开窗的时候同时，考虑像素值空间范围分布，只有符合分布的像素点才参与计算，计算得到像素均值与空间位置均值，
     使用新的均值位置作为窗口中心位置继续基于给定像素值空间分布计算均值与均值位置，
     如此不断迁移中心位置直到不再变化位置（dx=dy=0），但是在实际情况中我们会人为设置一个停止条件比如迁移几次，
     这样就可以把最后的RGB均值赋值给中心位置。

 OpenCV中均值迁移滤波的API函数：
 pyrMeanShiftFiltering(
     InputArray     src,
     OutputArray     dst,
     double     sp,
     double     sr,
     int     maxLevel = 1,
     TermCriteria  termcrit =
     TermCriteria(TermCriteria::MAX_ITER+TermCriteria::EPS, 5, 1)
 )
 */
namespace Day027 {
    void mainFunction(){
        Mat src = imread("./data/images/example.png");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        
        imshow("input", src);

        Mat dst;
        pyrMeanShiftFiltering(src, dst, 15, 30);
        imshow("result", dst);

        waitKey(0);
    }
}
