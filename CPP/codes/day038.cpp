//
//  day038.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/15.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day038-拉普拉斯金字塔
 对输入图像实现金字塔的reduce操作就会生成不同分辨率的图像、对这些图像进行金字塔expand操作，
 然后使用reduce减去expand之后的结果就会得到图像拉普拉斯金字塔图像。

 举例如下：
 输入图像G(0)
 金字塔reduce操作生成 G(1), G(2), G(3)
 拉普拉斯金字塔：
     L0 = G(0)-expand(G(1))
     L1 = G(1)-expand(G(2))
     L2 = G(2)–expand(G(3))

 G(0)减去expand(G(1))得到的结果就是两次高斯模糊输出的不同，所以L0称为DOG（高斯不同）、它约等于LOG所以又称为拉普拉斯金字塔。
 所以要求的图像的拉普拉斯金字塔，首先要进行金字塔的reduce操作，然后在通过expand操作，最后相减得到拉普拉斯金字塔图像。
 */
namespace Day038 {
    void mainFunction(){
        Mat src = imread("./data/images/lena.jpg");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        imshow("input", src);

        vector<Mat> images;
        char title[50];
        images = laplaian_pyramid(src, 3);
        for (Mat image : images) {
            sprintf(title, "laplaian_pyramid %dx%d", image.size().height, image.size().width);
            imshow(title, image);
        }

        waitKey(0);
    }
    vector<Mat> laplaian_pyramid(Mat src, int level){
        vector<Mat> gaussian_images, laplaian_pyramid;
            
        // reduce操作(高斯金字塔)
        Mat temp, dst;
        temp = src.clone();
        for (int i = 0; i < level; i++) {
            pyrDown(temp, dst);
            gaussian_images.push_back(dst);
            temp = dst.clone();
        }
            
        // 拉普拉斯金字塔
        // 生成G0
        pyrUp(gaussian_images[0], dst, src.size());
        subtract(src, dst, dst);
        dst = dst + Scalar(127, 127, 127);
        laplaian_pyramid.push_back(dst);
        for (int i = 0; i < level - 1; i++) {
            pyrUp(gaussian_images[i+1], dst, gaussian_images[i].size());
            subtract(gaussian_images[i], dst, dst);
            dst = dst + Scalar(127, 127, 127);
            laplaian_pyramid.push_back(dst);
        }
        return laplaian_pyramid;
    }
}
