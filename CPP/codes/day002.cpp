//
//  day02.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/1/24.
//

#include <stdio.h>

#include "toc.h"

using namespace cv;

namespace Day002 {
    void mainFunction(){
        Mat src = imread("./data/images/test.png");
        
        if(src.empty()){
            printf("could not load image...\n");
            return ;
        }
        
        namedWindow("day002", WINDOW_AUTOSIZE);
//        imshow("day002", src);
        
        Mat dst;
        cvtColor(src, dst, COLOR_BGR2GRAY);
        imshow("day002", dst);
        imwrite("./data/images/test_gray.png", dst);
        
        waitKey(0);
    }
}
