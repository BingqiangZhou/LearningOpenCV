//
//  day016.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/3.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day016-图像ROI与ROI操作
 图像的ROI(region of interest)是指图像中感兴趣区域、在OpenCV中图像设置图像ROI区域，实现只对ROI区域操作。

 1. 矩形ROI区域提取
 2. 矩形ROI区域copy
 3. 不规则ROI区域
     - ROI区域mask生成
     - 像素位 and操作
     - 提取到ROI区域
     - 加背景or操作
     - add 背景与ROI区域
 */
namespace Day016 {
    void mainFunction(){
        Mat src = imread("./data/images/cos.jpg");
        imshow("source image", src);

        // 提取ROI区域，将图像最中心的200x200区域作为ROI
        int h = src.rows;
        int w = src.cols;
        int cx = w / 2; // 图像中心点的x坐标
        int cy = h / 2; // 图像中心点的y坐标
        Rect rect(cx - 100, cy - 100, 200, 200); // (左上角x坐标，左上角y坐标，高，宽)
        Mat roi = src(rect);
        imshow("roi 200x200", roi);

        // roi依旧指向src对应的内存空间，对roi进行修改，则src也会被修改
        roi.setTo(Scalar(0, 0, 255));
        imshow("roi (0, 0, 255) image", src);

        // 复制roi，将roi与src对应的内存空间脱离，roi拥有对立的内存空间，对roi进行修改，则src不再会被修改
        Mat roi_new = roi.clone();
        // roi.copyTo(roi_new); 同上一行代码等效，不同的是roi_new需要copyTo先定义好
        roi_new.setTo(Scalar(255, 0, 0));
        imshow("roi_new image", src);

        Mat green_background_image = imread("./data/images/greenback.png");
        imshow("green background image", green_background_image);

        // 生成mask
        Mat hsv, mask;
        cvtColor(green_background_image, hsv, COLOR_BGR2HSV);
        inRange(green_background_image, Scalar(35, 43, 46), Scalar(99, 255, 255), mask); // 提取绿色（35-77，43-255，46-255）与青色（78-99，43-255，46-255）区域
        imshow("mask", mask);

        // 提取人的区域mask
        Mat person_mask;
        bitwise_not(mask, person_mask); // 注意这里的mask也会被改变为person_mask
        imshow("person mask", person_mask);
        
        // 获取彩色人形区域
        Mat person_image;
        bitwise_and(green_background_image, green_background_image, person_image, mask=person_mask);
        imshow("person image", person_image);

        // 生成新的背景
        Mat new_background = Mat::zeros(green_background_image.size(), CV_8UC3);
        new_background.setTo(Scalar(0, 255, 255));
        imshow("new background", new_background);
        
        // 读取图像作为新的背景
        // Mat new_background;
        // new_background = imread("./data/images/cos.jpg");
        // resize(new_background, new_background, green_background_image.size(), INTER_LINEAR);
        // imshow("new background", new_background);

        // 将背景中的人形部分去除
        Mat background_without_person_region;
        bitwise_not(person_mask, mask);
        bitwise_and(new_background, new_background, background_without_person_region, mask=mask);
        imshow("background_without_person_region", background_without_person_region);

        // 合并新的背景和人形区域
        Mat new_image;
        add(background_without_person_region, person_image, new_image); // 将去除人形部分的背景区域与彩色人形区域相加
        imshow("new image", new_image);

        waitKey(0);
        destroyAllWindows();
    }
}
