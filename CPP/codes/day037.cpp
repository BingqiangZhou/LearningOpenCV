//
//  day037.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/15.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day037-图像金字塔
 图像金字塔概念
     图像金字塔是对一张输入图像先模糊再下采样为原来大小的1/4（宽高缩小一半）、
     不断重复模糊与下采样的过程就得到了不同分辨率的输出图像，叠加在一起就形成了图像金字塔、
     所以图像金字塔是图像的空间多分辨率存在形式。
     这里的模糊是指高斯模糊，所以这个方式生成的金字塔图像又称为高斯金字塔图像。
 
 高斯金字塔图像有两个基本操作
     reduce 是从原图生成高斯金字塔图像、生成一系列低分辨图像
     expand是从高斯金字塔图像反向生成高分辨率图像

 规则：
     1.    图像金字塔在redude过程或者expand过程中必须是逐层
     2.    默认情况：reduce过程中每一层都是前一层的1/4（宽高缩小一半），expand过程中每一层都是前一层的4倍（宽高扩大一倍）

 相关API
     reduce 操作 pyrDown
     expand操作 pyrUp
 */
namespace Day037 {
    void mainFunction(){
        Mat src = imread("./data/images/lena.jpg");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        imshow("input", src);

        vector<Mat> up_pyramid, down_pyramid;
        up_pyramid = image_pyramid(src, 3, true);
        down_pyramid = image_pyramid(src, 3, false);
        
        char title[50];
        for (Mat image : up_pyramid) {
            sprintf(title, "up_pyramid %dx%d", image.size().height, image.size().width);
            imshow(title, image);
        }
        
        for (Mat image : down_pyramid) {
            sprintf(title, "down_pyramid %dx%d", image.size().height, image.size().width);
            imshow(title, image);
        }
        
        waitKey(0);
    }
    vector<Mat> image_pyramid(Mat src, int level, bool upsample){
        vector<Mat> pyramid_images;
        Mat temp = src.clone();
        Mat dst;
        for (int i = 0; i < level; i++) {
            if(upsample == true){
                pyrUp(temp, dst);
            }
            else{
                pyrDown(temp, dst);
            }
            temp = dst.clone();
            pyramid_images.push_back(temp);
        }
        return pyramid_images;
    }
}
