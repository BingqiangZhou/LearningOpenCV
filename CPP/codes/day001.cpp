//
//  day01.cpp
//  Learning_OpenCV
//
//  Created by bingqiangzhou on 2021/1/24.
//

#include "toc.h"

#include <stdio.h>

using namespace cv;

namespace Day001 {
    void mainFunction(){
//        Mat src = imread("./data/images/test.png");
        Mat src = imread("./data/images/test.png", IMREAD_GRAYSCALE);
        
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        namedWindow("hello, opencv", WINDOW_AUTOSIZE);
        imshow("hello, opencv", src);
        
        waitKey(0);
    }
}
