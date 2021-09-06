//
//  day025.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/11.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day025-图像去噪声
 图像去噪声在OCR、机器人视觉与机器视觉领域应用开发中是重要的图像预处理手段之一，对图像二值化与二值分析很有帮助.
 OpenCV中常见的图像去噪声的方法有
 - 均值去噪声
 - 高斯模糊去噪声
 - 非局部均值去噪声
 - 双边滤波去噪声 (后面再介绍)
 - 形态学去噪声 (后面再介绍)
 一般卷积核大小从3x3尝试起，卷积核大小不易过大，过大会丢失大量图像原有细节。
 */
namespace Day025 {
    void mainFunction(){
        Mat src = imread("./data/images/lena.jpg");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        
        Mat dst_salt_pepper = generateSaltPepperNoise(src);
        Mat dst_gaussian = generateGaussianNoise(src);
        
        // 均值模糊
        Mat dst_salt_pepper_blur, dst_gaussian_blur;
        blur(dst_salt_pepper, dst_salt_pepper_blur, Size(5, 5));
        blur(dst_gaussian, dst_gaussian_blur, Size(5, 5));

        // 中值模糊，ksize为大于1的奇数
        Mat dst_salt_pepper_median, dst_gaussian_blur_median;
        medianBlur(dst_salt_pepper, dst_salt_pepper_median, 5);
        medianBlur(dst_gaussian_blur, dst_gaussian_blur_median, 5);

        // 高斯模糊
        Mat dst_salt_pepper_gaussian, dst_gaussian_blur_gaussian;
        GaussianBlur(dst_salt_pepper, dst_salt_pepper_gaussian, Size(5, 5), 15);
        GaussianBlur(dst_gaussian_blur, dst_gaussian_blur_gaussian, Size(5, 5) , 15);

        // 非局部均值去噪，搜索框一般是模版框大小的3倍
        Mat dst_salt_pepper_nlmean, dst_gaussian_blur_nlmean;
        fastNlMeansDenoisingColored(dst_salt_pepper, dst_salt_pepper_nlmean, 15, 15, 10, 30);
        fastNlMeansDenoisingColored(dst_gaussian_blur, dst_gaussian_blur_nlmean, 15, 15, 10, 30);

        // 可视化
        // imshow("original image", src)
        imshow("dst_salt_pepper", dst_salt_pepper);
        imshow("dst_gaussian", dst_gaussian);
        imshow("dst_salt_pepper_blur", dst_salt_pepper_blur);
        imshow("dst_gaussian_blur", dst_gaussian_blur);
        imshow("dst_salt_pepper_median", dst_salt_pepper_median);
        imshow("dst_gaussian_blur_median", dst_gaussian_blur_median);
        imshow("dst_salt_pepper_gaussian", dst_salt_pepper_gaussian);
        imshow("dst_gaussian_blur_gaussian", dst_gaussian_blur_gaussian);
        imshow("dst_salt_pepper_nlmean", dst_salt_pepper_nlmean);
        imshow("dst_gaussian_blur_nlmean", dst_gaussian_blur_nlmean);
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
