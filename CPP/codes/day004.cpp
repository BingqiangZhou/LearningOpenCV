//
//  day004.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/1/24.
//

#include <stdio.h>

#include "toc.h"

using namespace cv;

/* Day004-C++中的像素遍历与访问
 数组遍历 - src.at<T>(row, col)
 指针方式遍历 - src.ptr<T>(row)
 */
namespace Day004 {
    void mainFunction(){
        Mat src = imread("./data/images/test.png");
        
        if(src.empty()){
            printf("could not load image...\n");
            return ;
        }
        
        // 数组遍历
        Mat m1 = arrayTraveral(src);
//        namedWindow("arrayTraveral");
        imshow("arrayTraveral", m1);
        
        // 指针方式遍历
        Mat m2 = pointerTraversal(src);
//        namedWindow("pointerTraversal");
        imshow("pointerTraversal", m2);
        waitKey(0);
    };

    // 数组遍历
    Mat arrayTraveral(Mat src){
        int h = src.rows;
        int w = src.cols;
        int c = src.channels();
        
        for (int row = 0; row < h; row++) {
            for (int col = 0; col < w; col++) {
                if(c == 3){
                    // typedef Vec<uchar, 3> cv::Vec3b, 3个uchar的向量（数组）
                    // u: uchar, b: uchar, d: double, f: float, i: int, s: short, w: ushort;
                    Vec3b bgr = src.at<Vec3b>(row, col);
                    bgr[0] = 255 - bgr[0];
                    bgr[1] = 255 - bgr[1];
                    bgr[2] = 255 - bgr[2];
                    src.at<Vec3b>(row, col) = bgr;
                } else if (c == 1){
                    int gray = src.at<uchar>(row, col);
                    src.at<uchar>(row, col) = 255 - gray;
                }
            }
        }
        
        return src;
    };

    // 指针方式遍历
    Mat pointerTraversal(Mat src){
        int h = src.rows;
        int w = src.cols;
        int c = src.channels();
        
//        int b = 0, g = 0, r = 0;
//        int gary = 0;
        
        Mat result = Mat::zeros(h, w, src.type());
        
        for (int row = 0; row < h; row++) {
            uchar* curr_row = src.ptr<uchar>(row); // 获取到当前行的首地址
            uchar* result_row = result.ptr<uchar>(row);
            for (int col = 0; col < w; col++) {
//                if (c == 3) { // bgr
//                    // b, g, r是被顺序存储的
//                    b = *curr_row++;
//                    g = *curr_row++;
//                    r = *curr_row++;
//
//                    *result_row++ = 255 - b;
//                    *result_row++ = 255 - g;
//                    *result_row++ = 255 - r;
//                }else if (c == 1){ // gray
//                    gary = *curr_row++;
//                    *result_row++ = 255 - gary;
//                }
                
                // 上面75-87行代码 可用 下面的for循环的代码 代替
                for(int i = 0; i < c; i++){
                    *result_row++ = 255 - *curr_row++;
                }
            }
        }
        
        return result;
    };
}
