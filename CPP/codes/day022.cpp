//
//  day022.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/10.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day002-图像均值模糊与高斯模糊
 均值模糊 卷积核的系数完全一致，
 高斯模糊考虑了中心像素距离的影响，对距离中心像素使用高斯分布公式生成不同的权重系数给卷积核，
     然后用此卷积核完成图像卷积得到输出结果就是图像高斯模糊之后的输出。
 OpenCV高斯模糊 API函数
     void GaussianBlur(
         InputArray src,
         OutputArray dst,
         Size ksize, // Ksize为高斯滤波器窗口大小
         double sigmaX, // 高斯核在x方向的标准差
         double sigmaY=0, // 高斯核在y方向的标准差
         int borderType=BORDER_DEFAULT // 默认边缘插值方法
         )
 关于参数ksize：
     ksize.width和ksize.height可以不同
     取值有2种情况：
     可以是正的奇数
     也可以是0，此时它们的值会自动由sigma进行计算
 关于参数sigmaX和sigmaY：
     sigmaY=0时，其值自动由sigmaX确定（sigmaY=sigmaX）；
     sigmaY=sigmaX=0时，它们的值将由ksize.width和ksize.height自动确定；
 
 ksize 越大，他的模糊程度越大，sigma越大，模糊程度也越大。
 */
namespace Day022 {
    void mainFunction(){
        Mat src = imread("./data/images/snow.png");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }

        Mat dst1, dst2;
        blur(src, dst1, Size(5, 5), Point(-1, -1), 4);
        GaussianBlur(src, dst2, Size(5, 5), 15, 0, 4);

        imshow("src", src);
        imshow("blur", dst1);
        imshow("gaussian blur", dst2);
        
        waitKey(0);
    }
}
