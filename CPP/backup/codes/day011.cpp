//
//  day011.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/1.
//

#include <stdio.h>

#include "toc.h"

using namespace cv;
using namespace std;

/** Day011-像素归一化
 OpenCV中四种归一化的方法
 - NORM_MINMAX      x = beta + (alpha - beta) * ( (x - min) / (max - min))
 - NORM_INF               x = alpha *  x / max
 - NORM_L1                 x = alpha * x / \sum(|x_i|) 除以L1-范数
 - NORM_L2                 x =  alpha * x / \sqrt(\sum(|x_i^2|)) 除以L2-范数
 最常用的就是NORM_MINMAX归一化方法。

 相关API函数：
 normalize(
 InputArray     src, // 输入图像
 InputOutputArray     dst, // 输出图像
 double     alpha = 1, // NORM_MINMAX时候低值
 double     beta = 0, // NORM_MINMAX时候高值
 int     norm_type = NORM_L2, // 只有alpha
 int     dtype = -1, // 默认类型与src一致
 InputArray     mask = noArray() // mask默认值为空
 )
 */
namespace Day011 {
    void mainFunction(){
        
        vector<double> data = { 2.0, 8.0, -1.0};
        
        Mat src = imread("./data/images/cos.jpg");
        imshow("source image", src);
        
        src.convertTo(src, CV_32FC3); // 归一化之前需要将整数类型转换为浮点数类型，不然归一化之后会被截断，值变成0。
        
        Mat dst;
        vector<double> v_dst;
        
        // NORM_L1
        normalize(data, v_dst, 1, 0, NORM_L1);
        printVector(v_dst, "NORM_L1"); // 0.181818, 0.727273, -0.090909,
        
        normalize(src, dst, 1, 0, NORM_L1);
        Mat temp = dst * 1e8; // 归一化之后的值过小，乘以一个合适的值，便于可视化。
        temp.convertTo(dst, CV_8UC3); // 便于可视化，做数值类型转换
        imshow("NORM_L1", dst);
        
        // NORM_L2
        normalize(data, v_dst, 1, 0, NORM_L2);
        printVector(v_dst, "NORM_L2"); // 0.240772, 0.963087, -0.120386
        
        normalize(src, dst, 1, 0,NORM_L2);
        temp = dst * 1e5; // 归一化之后的值过小，乘以一个合适的值，便于可视化。
        temp.convertTo(dst, CV_8UC3); // 便于可视化，做数值类型转换
        imshow("NORM_L2", dst);
        
        // NORM_INF
        normalize(data, v_dst, 1, 0, NORM_INF);
        printVector(v_dst, "NORM_INF"); // 0.250000, 1.000000, -0.125000,
        
        normalize(src, dst, 1, 0, NORM_INF);
        temp = dst * 255;
        temp.convertTo(dst, CV_8UC3); // 便于可视化，做数值类型转换
        imshow("NORM_INF", dst);
        
        // NORM_MINMAX
        normalize(data, v_dst, 1, 0, NORM_MINMAX);
        printVector(v_dst, "NORM_MINMAX"); // 0.333333, 1.000000, 0.000000,
        
        normalize(src, dst, 1, 0, NORM_MINMAX);
        temp = dst * 255;
        temp.convertTo(dst, CV_8UC3); // 便于可视化，做数值类型转换
        imshow("NORM_MINMAX", dst);
        
        normalize(data, v_dst, 0, 1, NORM_MINMAX); // alpha, beta参数值，那个大那个为alpha，无关顺序
        printVector(v_dst, "NORM_MINMAX"); // 0.333333, 1.000000, 0.000000,
        
        waitKey(0);
    };
    //输出Vector中的数据
    void printVector(vector<double> list, string title){
        cout << title;
        for (double v : list) {
            printf(" %.6f,", v);
        }
        cout << endl;
    }
}
