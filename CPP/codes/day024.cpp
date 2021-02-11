//
//  day024.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/11.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day024-图像噪声
 图像噪声产生的原因很复杂，有的可能是数字信号在传输过程中发生了丢失或者受到干扰，
     有的是成像设备或者环境本身导致成像质量不稳定，反应到图像上就是图像的亮度与颜色呈现某种程度的不一致性。
 从噪声的类型上，常见的图像噪声可以分为如下几种:
     - 椒盐噪声，
     是一种随机在图像中出现的稀疏分布的黑白像素点， 对椒盐噪声一种有效的去噪手段就是图像中值滤波

     - 高斯噪声/符合高斯分布
     一般会在数码相机的图像采集(acquisition)阶段发生,这个时候它的物理/电/光等各种信号都可能导致产生高斯分布噪声。

     - 均匀分布噪声
     均匀/规则噪声一般都是因为某些规律性的错误导致的
 代码演示
 - 图像椒盐噪声生成
 - 图像高斯噪声生成
 */
namespace Day024 {
    void mainFunction(){
        Mat src = imread("./data/images/lena.jpg");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        
        Mat dst_salt_pepper = generateSaltPepperNoise(src);
        Mat dst_gaussian = generateGaussianNoise(src);
        
        imshow("original image", src);
        imshow("salt pepper noise", dst_salt_pepper);
        imshow("gaussian noise", dst_gaussian);
        
        waitKey(0);
        destroyAllWindows();
    }
    Mat generateSaltPepperNoise(Mat image){
        RNG rng(0xffffffff);
        Mat dst = image.clone();
        int h = dst.rows;
        int w = dst.cols;
        int nums = 10000;
        for (int i = 0; i < nums; i++) {
            int x = rng.uniform(0, w);
            int y = rng.uniform(0, h);
            if (i % 2 == 1) {
                dst.at<Vec3b>(y, x) = Vec3b(255, 255, 255);
            }
            else {
                dst.at<Vec3b>(y, x) = Vec3b(0, 0, 0);
            }
        }
        return dst;
    }
    Mat generateGaussianNoise(Mat image){
        Mat noise = Mat::zeros(image.size(), image.type());
        randn(noise, Scalar(15, 15, 15), Scalar(30, 30, 30));
        Mat dst;
        add(image, noise, dst);
        return dst;
    }
}
