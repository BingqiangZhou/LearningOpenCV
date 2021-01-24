//
//  day001.cpp
//  Learning_OpenCV
//
//  Created by bingqiangzhou on 2021/1/24.
//

#include <stdio.h>

#include "toc.h"

using namespace cv;

/* Day001-图像读取与显示
读取图像 - imread
显示图像 - imshow
 */
namespace Day001 {
    void mainFunction(){
        // Mat src = imread("./data/images/test.png");
        Mat src = imread("./data/images/test.png", IMREAD_GRAYSCALE);
        
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        
        // namedWindow可以省略，窗口默认大小是自适应大小WINDOW_AUTOSIZE
        // namedWindow("hello, opencv", WINDOW_AUTOSIZE);
        imshow("hello, opencv", src);
        
        waitKey(0);
    }
}
