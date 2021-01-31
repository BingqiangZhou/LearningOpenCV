//
//  day008.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/1/31.
//

#include <stdio.h>


#include <string>
#include "toc.h"

using namespace cv;
using namespace std;

/* Day008-图像通道分离与合并
 通道分离 - split
 通道合并 - merge
 混合通道 - mixChannels 将输入数组的指定通道复制到输出数组的指定通道
 */
namespace Day008 {
    void mainFunction(){
        Mat src = imread("./data/images/cos.jpg");
//        Mat src = imread("./data/images/flower.png");
        imshow("source image", src);
        
        vector<Mat> mat_list;
        
        // 通道分离
        split(src, mat_list);
        for (int i = 0; i < mat_list.size(); i++) {
            imshow("image channel " + to_string(i), mat_list[i]);
        }
        
        // 通道合并，将一个通道所有值设置为0再合并
        for (int i = 0; i < 3; i++) {
            Mat dst;
            vector<Mat> temp;
            split(src, temp);
            temp[i] = Scalar(0); // 将第i个通道置为0
            merge(temp, dst);
            imshow("merge image channel without channel " + to_string(i), dst);
        }
        
        // 混合通道 - 将输入数组的指定通道复制到输出数组的指定通道
        Mat dst = Mat::zeros(src.size(), CV_8UC3);// 需要初始化输出的Mat与输入的Mat同大小
        vector<int> from_to{0, 1, 1, 2, 2, 0}; // 两个两个一组，0，1；1，2；2，0，src的第一个通道放到dst第二个换，src的第二个通道与放到dst第三个，src的第三个通道与放到dst第一个通道
        mixChannels(src, dst, from_to);
        imshow("image mixChannels ", dst);
        
        // mixChannels 还有以下两种形式，可以将Mat数组作为输入输出 参考链接：https://docs.opencv.org/master/d2/de8/group__core__array.html#ga51d768c270a1cdd3497255017c4504be
        // void cv::mixChannels(const Mat *src, size_t nsrcs,Mat * dst,size_t ndsts,const int *fromTo,size_t npairs)
        // void cv::mixChannels(InputArrayOfArrays src, InputOutputArrayOfArrays dst, const int *fromTo, size_t npairs)
        
        waitKey(0);
    }
}
