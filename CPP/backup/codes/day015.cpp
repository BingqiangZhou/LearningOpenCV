//
//  day015.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/2.
//

#include <stdio.h>

#include "toc.h"

using namespace std;
using namespace cv;

/**Day015-几何形状绘制
 绘制几何形状
     - 绘制直线
     - 绘制圆
     - 绘制矩形
     - 绘制椭圆
 填充几何形状
     OpenCV没有专门的填充方法，只是把绘制几何形状时候的线宽 - thickness参数值设置为负数即表示填充该几何形状或者使用参数CV_FILLED
     线的类型有3种：LINE_4（四邻域）、LINE_8（8邻域）、LINE_AA （抗锯齿，antialiased）
 随机数方法：
     RNG(Random Number Generator) 表示OpenCV C++版本中的随机数对象，rng.uniform(a, b)生成[a, b)之间的随机数，包含a，但是不包含b。
     np.random.rand() 表示numpy中随机数生成，生成浮点数0～1的随机数, 包含0，不包含1。
 */
namespace Day015 {
    void mainFunction(){
        Mat canvas = Mat::zeros(Size(512, 512), CV_8UC3);

        // 画线 (图像对象，起始点，结束点，bgr颜色，线宽，线的类型，点坐标中的二进制右移位数)
        // thickness参数值设置为负数即表示填充该几何形状或者使用参数CV_FILLED
        // 线的类型有3种：LINE_4（四邻域）、LINE_8（8邻域）、LINE_AA （抗锯齿，antialiased）
        // shift是将坐标值二进制右移的位数, v/(2**shift)
        line(canvas, Point(0, 0), Point(512, 512), Scalar(0, 0, 255), 10, LINE_4, 0);
        
        // 画矩形 参数与画线一致 (图像对象，起始点，结束点，bgr颜色，线宽，线的类型，点坐标中的二进制右移位数)，起始坐标（8， 8）结束坐标（256， 256）
        rectangle(canvas, Point(64, 64), Point(1024, 1024), Scalar(0, 255, 0), 3, LINE_8, 2);

        // 画圆 (图像对象，圆心，半径，bgr颜色，线宽，线的类型，点坐标中的二进制右移位数)
        circle(canvas, Point(256, 256), 200, Scalar(255, 0, 0), 5, LINE_8, 0);

        // 画椭圆 (图像对象，圆心，水平轴与竖直轴长度，画多少度，开始画的角度，结束的角度，bgr颜色，线宽，线的类型，点坐标中的二进制右移位数)
        ellipse(canvas, Point(256, 256), Size(150, 200), 360, 0, 360, Scalar(255, 255, 0), -1, LINE_AA, 0);
        ellipse(canvas, Point(256, 256), Size(200, 150), 360, 0, 360, Scalar(255, 255, 0), FILLED, LINE_AA, 0);

        imshow("canvas", canvas);

        // 重置画布（将图像三个通道都置为0）
        canvas.setTo(Scalar(0, 0, 0));

        // 随机画线(画矩形)的位置、颜色
        int h = canvas.rows;
        int w = canvas.cols;
        
        int x1, y1, x2, y2, b, g, r;
        RNG rng(0xffffff); // 初始化
        for (int i = 0; i < 1e3; i++) {
            // canvas.setTo(Scalar(0, 0, 0));
            
            // 随机起始坐标、结束坐标
            x1 = rng.uniform(0, w);
            y1 = rng.uniform(0, h);
            x2 = rng.uniform(0, w);
            y2 = rng.uniform(0, h);

            // 随机颜色值
            b = rng.uniform(0, 256);
            g = rng.uniform(0, 256);
            r = rng.uniform(0, 256);

            line(canvas, Point(x1, y1), Point(x2, y2), Scalar(b, g, r), 1, LINE_8, 0);
            // rectangle(canvas, Point(x1, y1), Point(x2, y2), Scalar(b, g, r), 1, LINE_8, 0);

            imshow("random draw", canvas);

            char c = waitKey(10);
            if (c == 27) { // ESC
                break;
            }
        }
            
        waitKey(0);
        destroyAllWindows();
    }
}
