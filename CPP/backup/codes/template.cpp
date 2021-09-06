//
//  template.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/17.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

void mainFunction(){
    Mat src = imread("./data/images/lena.jpg");
    if (src.empty()) {
        printf("could not load image...\n");
        return ;
    }
    imshow("original", src);

    waitKey(0);
}
