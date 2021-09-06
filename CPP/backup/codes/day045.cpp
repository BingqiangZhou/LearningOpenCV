//
//  day045.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/17.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day045-图像二值化与去噪
 对于一张需要二值化的图像，我们有两种选择
 选择一
     直接对输入图像转换为灰度图像，然后二值化
 选择二
     首先对输入图像进行降噪，去除噪声干扰，然后再二值化

 在进行去噪声的时候，还记得前面我们分享的几种去噪声方法，可以选择的有
 均值模糊去噪声
 高斯模糊去噪声
 双边/均值迁移模糊去噪声
 非局部均值去噪声
 */
namespace Day045 {
    void mainFunction(){
        Mat src = imread("./data/images/coins.jpg");
        if (src.empty()) {
            printf("could not load image...\n");
            return ;
        }
        // 直接对输入图像转换为灰度图像，然后二值化
        Mat gray;
        cvtColor(src, gray, COLOR_BGR2GRAY);
        imshow("original gray", gray);

        Mat binary;
        double thresh = threshold(gray, binary, 0, 255, THRESH_OTSU);
        cout << "threshold: " << thresh << endl;
        imshow("THRESH_OTSU", binary);
        
        // 首先对输入图像进行降噪，去除噪声干扰，然后再二值化
        Mat blured, blured_gray;
        // 1. 均值模糊去噪声
        blur(src, blured, Size(3, 3));
        cvtColor(blured, blured_gray, COLOR_BGR2GRAY);
        thresh = threshold(blured_gray, binary, 0, 255, THRESH_OTSU);
        cout << "threshold: " << thresh << endl;
        imshow("blur OTSU", binary);

        // 2. 高斯模糊去噪声
        GaussianBlur(src, blured, Size(3, 3), 0);
        cvtColor(blured, blured_gray, COLOR_BGR2GRAY);
        thresh = threshold(blured_gray, binary, 0, 255, THRESH_OTSU);
        cout << "threshold: " << thresh << endl;
        imshow("GaussianBlur OTSU", binary);
        
        // 3. 双边模糊去噪声
        bilateralFilter(src, blured, -1, 100, 10);
        cvtColor(blured, blured_gray, COLOR_BGR2GRAY);
        thresh = threshold(blured_gray, binary, 0, 255, THRESH_OTSU);
        cout << "threshold: " << thresh << endl;
        imshow("bilateralFilter OTSU", binary);

        // 4. 均值迁移模糊去噪声
        pyrMeanShiftFiltering(src, blured, 10, 100);
        cvtColor(blured, blured_gray, COLOR_BGR2GRAY);
        thresh = threshold(blured_gray, binary, 0, 255, THRESH_OTSU);
        cout << "threshold: " << thresh << endl;
        imshow("pyrMeanShiftFiltering OTSU", binary);

        // 5. 非局部均值去噪声
        fastNlMeansDenoisingColored(src, blured);
        cvtColor(blured, blured_gray, COLOR_BGR2GRAY);
        thresh = threshold(blured_gray, binary, 0, 255, THRESH_OTSU);
        cout << "threshold: " << thresh << endl;
        imshow("fastNlMeansDenoisingColored OTSU", binary);
        
        waitKey(0);
    }
}
