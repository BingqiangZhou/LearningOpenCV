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

// Day019-图像直方图比较
namespace Day019 {
    void mainFunction();
}

// Day020-图像直方图反向投影
namespace Day020 {
    void mainFunction();
    void backProject(cv::Mat roi_image, cv::Mat target_model, bool show_fig=true);
}

// Day021-图像卷积操作
namespace Day021 {
    void mainFunction();
    cv::Mat custom_3x3_blur(cv::Mat src);
}

// Day002-图像均值模糊与高斯模糊
namespace Day022 {
    void mainFunction();
}

// Day023-图像中值模糊
namespace Day023 {
    void mainFunction();
}

// Day024-图像噪声
namespace Day024 {
    void mainFunction();
    cv::Mat generateSaltPepperNoise(cv::Mat image);
    cv::Mat generateGaussianNoise(cv::Mat image);
}

// Day025-图像去噪声
namespace Day025 {
    void mainFunction();
    cv::Mat generateSaltPepperNoise(cv::Mat image);
    cv::Mat generateGaussianNoise(cv::Mat image);
}

// Day026-边缘保留滤波算法 – 高斯双边模糊
namespace Day026 {
    void mainFunction();
}

// Day027-边缘保留滤波算法 – 均值迁移模糊(mean-shift blur)
namespace Day027 {
    void mainFunction();
}

// Day028-图像积分图算法
namespace Day028 {
    void mainFunction();
    // 通过和(sum)表来计算均值模糊
    cv::Mat blur_demo(cv::Mat &image, cv::Mat &sum);
    // 根据和（sum）表计算卷积框内的像素值的和
    int getblockSum(cv::Mat &sum, int x1, int y1, int x2, int y2, int i);
}

// Day029-快速的图像边缘滤波算法
namespace Day029 {
    void mainFunction();
}

// Day030-OpenCV中的自定义滤波器
namespace Day030 {
    void mainFunction();
}

// Day031-图像梯度 – Sobel算子
namespace Day031 {
    void mainFunction();
}

// Day032-图像梯度 – 更多梯度算子
namespace Day032 {
    void mainFunction();
}

// Day033-图像梯度 – 拉普拉斯算子(二阶导数算子)
namespace Day033 {
    void mainFunction();
}

// Day034-图像锐化
namespace Day034 {
    void mainFunction();
}

// Day035-USM 锐化增强算法
namespace Day035 {
    void mainFunction();
}

// Day036-Canny边缘检测器
namespace Day036 {
    void mainFunction();
}

// Day037-图像金字塔
namespace Day037 {
    void mainFunction();
    std::vector<cv::Mat> image_pyramid(cv::Mat src, int level, bool upsample);
}

// Day038-拉普拉斯金字塔
namespace Day038 {
    void mainFunction();
    std::vector<cv::Mat> laplaian_pyramid(cv::Mat src, int level);
}

// Day039-图像模板匹配
namespace Day039 {
    void mainFunction();
}

#endif /* toc_h */
