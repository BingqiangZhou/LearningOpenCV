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
    cv::Mat pointerTraversal(cv::Mat src); // 指针方式遍历
}

/* Day005-图像像素的算术操作
 加add、减subtract、乘multiply、除divide
 防止数据越界 saturate_cast
 */
namespace Day005 {
    void mainFunction();
    void addImplementByArray(cv::Mat m1, cv::Mat m2, cv::Mat result); // 自行实现加操作(数组遍历)
    void addImplementByPointer(cv::Mat m1, cv::Mat m2, cv::Mat result); // 自行实现加操作（指针遍历）
}

/* Day006-LUT(Look Up Table, 查找表)的作用与用法
 applyColorMap(src, dst, COLORMAP)
     - src 表示输入图像
     - dst表示输出图像
     - 匹配到的颜色LUT， OpenCV支持13种颜色风格的查找表映射
 */
namespace Day006 {
    void mainFunction();
    void customColorMap(cv::Mat &image);
}

/* Day007-图像像素的逻辑操作
 - bitwise_and 与
 - bitwise_xor 异或
 - bitwise_or  或
 上面三个类似，都是针对两张图像的位操作

 - bitwise_not 非
 针对输入图像, 图像取反操作，二值图像分析中经常用
 */
namespace Day007 {
    void mainFunction();
}

/* Day008-图像通道分离与合并
 通道分类 - split
 通道合并 - merge
 混合通道 - mixChannels 将输入数组的指定通道复制到输出数组的指定通道
 */
namespace Day008 {
    void mainFunction();
}

/* Day009-图像色彩空间转换
 色彩空间与色彩空间转换
 - RGB色彩空间  (red, green, blue)
 - HSV色彩空间  (Hue色调, Saturation饱和度, Value明度)，参考：https://zh.wikipedia.org/zh-hans/HSL和HSV色彩空间
 - YUV色彩空间  (Y 明亮度（Luminance、Luma），U和V則是色度（Chrominance、Chroma)参考：https://zh.wikipedia.org/wiki/YUV
 - YCrCb色彩空间 是YUV压缩和偏移的版本，参考：https://zh.wikipedia.org/wiki/YCbCr

 API知识点
 - 色彩空间转换cvtColor
 - 提取指定色彩范围区域inRange
 */
namespace Day009 {
    void mainFunction();
}

/* Day010-图像像素值统计
 像素值统计
 - 最小(min)
 - 最大(max)
 - 均值(mean)
 - 标准方差(standard deviation)

 API
 - 最大最小值minMaxLoc
 - 计算均值与标准方差meanStdDev
 */
namespace Day010 {
    void mainFunction();
}


#endif /* toc_h */
