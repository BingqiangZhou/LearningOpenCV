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

// Day001-图像读取与显示
namespace Day001 {
    void mainFunction();
}

// Day002-图像色彩空间转换
namespace Day002 {
    void mainFunction();
}

// Day003-OpenCV中图像对象创建与赋值
namespace Day003 {
    void mainFunction();
}

// Day004-C++中的像素遍历与访问
namespace Day004 {
    void mainFunction();
    cv::Mat arrayTraveral(cv::Mat src); // 数组遍历
    cv::Mat pointerTraversal(cv::Mat src); // 指针方式遍历
}

// Day005-图像像素的算术操作
namespace Day005 {
    void mainFunction();
    void addImplementByArray(cv::Mat m1, cv::Mat m2, cv::Mat result); // 自行实现加操作(数组遍历)
    void addImplementByPointer(cv::Mat m1, cv::Mat m2, cv::Mat result); // 自行实现加操作（指针遍历）
}

// Day006-LUT(Look Up Table, 查找表)的作用与用法
namespace Day006 {
    void mainFunction();
    void customColorMap(cv::Mat &image);
}

// Day007-图像像素的逻辑操作
namespace Day007 {
    void mainFunction();
}

// Day008-图像通道分离与合并
namespace Day008 {
    void mainFunction();
}

// Day009-图像色彩空间转换
namespace Day009 {
    void mainFunction();
}

// Day010-图像像素值统计
namespace Day010 {
    void mainFunction();
}

// Day011-像素归一化
namespace Day011 {
    void mainFunction();
    void printVector(std::vector<double> list, std::string title="values");//输出Vector中的数据
}

// Day012-视频读写
namespace Day012 {
    void mainFunction();
}

// Day013-图像翻转(Image Flip)
namespace Day013 {
    void mainFunction();
}

// Day014-图像插值(Image Interpolation)
namespace Day014 {
    void mainFunction();
}

// Day015-几何形状绘制
namespace Day015 {
    void mainFunction();
}

// Day016-图像ROI与ROI操作
namespace Day016 {
    void mainFunction();
}

// Day017-图像直方图
namespace Day017 {
    void mainFunction();
    void showHist(cv::Mat hist, std::string title="hist");
    void showHist(std::vector<cv::Mat> hist_list, std::string title="hist");
}

// Day018-图像直方图均衡化
namespace Day018 {
    void mainFunction();
}

/**Day019-图像直方图比较
 图像直方图比较，就是计算两幅图像的直方图数据，比较两组数据的相似性，从而得到两幅图像之间的相似程度，
 直方图比较在早期的CBIR(Content-based image retrieval, 基于内容的图像检索 )中是应用很常见的技术手段，
 通常会结合边缘处理、词袋等技术一起使用。

 OpenCV中直方图比较的API很简单
 compareHist(hist1, hist2, method)
     -常见比较方法有
         相关性：越接近+1越相似，越不相似越接近-1
         卡方： 值越小越相似
         交叉：不太准
         巴氏距离：越接近0则越相似
     具体公式可见：HistCompMethods，https://docs.opencv.org/master/d6/dc7/group__imgproc__hist.html#ga994f53817d621e2e4228fc646342d386
 */
namespace Day019 {
    void mainFunction();
}

#endif /* toc_h */
