//
//  toc.h
//  Learning_OpenCV
//
//  Created by bingqiangzhou on 2021/1/24.
//
// Table of Contents

#ifndef toc_h
#define toc_h

#include <opencv2/opencv.hpp>

/* Day001-图像读取与显示
读取图像 - imread
显示图像 - imshow
 */
namespace Day001 {
    void mainFunction();
}


/* Day002-图像色彩空间转换
色彩空间转换函数 - cvtColor
图像保存 - imwrite
 */
namespace Day002 {
    void mainFunction();
}


/* Day003-OpenCV中图像对象创建与赋值
C++中Mat对象与创建 - clone, copyTo, zeros, ones, eye
 */
namespace Day003 {
    void mainFunction();
}

/* Day004-C++中的像素遍历与访问
 数组遍历
 指针方式遍历
 */
namespace Day004 {
    void mainFunction();
    cv::Mat arrayTraveral(cv::Mat src); // 数组遍历
    cv::Mat pointerTraversal(cv::Mat src);
}


#endif /* toc_h */
