//
//  day014.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/2.
//

#include <stdio.h>

#include "toc.h"

using namespace cv;
using namespace std;


/**Day014-图像插值(Image Interpolation)
 最常见四种插值算法
     INTER_NEAREST = 0
     INTER_LINEAR = 1
     INTER_CUBIC = 2
     INTER_LANCZOS4 = 4
 相关的应用场景
     几何变换、透视变换、插值计算新像素
 resize,
     如果size有值，使用size做放缩插值，否则根据fx与fy
     另外需要注意的是opencv中的Size是(col, row)即(w, h)
     根据fx与fy的size=(cols * fx, rows * fy)，并向下取整
 相关参考链接：
     几种插值算法对比研究 - https://blog.csdn.net/Trent1985/article/details/45150677
     图像处理之三种常见双立方插值算法 - https://blog.csdn.net/jia20003/article/details/40020775
     图像放缩之双立方插值 - https://blog.csdn.net/jia20003/article/details/6919845
     图像放缩之双线性内插值 - https://blog.csdn.net/jia20003/article/details/6915185
     图像处理之Lanczos采样放缩算法 - https://blog.csdn.net/jia20003/article/details/17856859
 */
namespace Day014 {
    void mainFunction(){
        Mat src = imread("./data/images/cos.jpg");
        cout << "source image: " << src.size() << endl; // 列x行 [576 x 360]
        imshow("source image", src);

        int h = src.rows;
        int w = src.cols;
        Mat dst;
        
        // 最近邻插值方法，resize大小为原图想大小的两倍，需要注意的是opencv中的Size是(col, row)即(w, h)
        resize(src, dst, Size(w * 2, h * 2), 0, 0 , INTER_NEAREST);
        cout << "INTER_NEAREST: " << dst.size() << endl; // 列x行 [1152 x 720]
        imshow("INTER_NEAREST", dst);

        // 双线性插值方法，resize大小为(500, 500)
        resize(src, dst, Size(500, 500), 0, 0, INTER_LINEAR);
        cout << "INTER_LINEAR: " << dst.size() << endl; // 列x行 [500 x 500]
        imshow("INTER_LINEAR", dst);

        // 双线性三次插值方法（立方卷积插值)，resize为原图大小宽高(列行)的0.5倍（w * 0.5，h * 0.5）(向下取整)
        resize(src, dst, Size(0, 0), 0.5, 0.5, INTER_CUBIC);
        cout << "INTER_CUBIC: " << dst.size() << endl; // 列x行 [288 x 180]
        imshow("INTER_CUBIC", dst);

        // Lanczos插值方法，resize为原图大小（w * 1.5，h * 0.5）,当size有值时，使用size做放缩插值，fx与fy不生效
        resize(src, dst, Size(int(w * 1.5), int(h * 0.5)), 1, 1, INTER_LANCZOS4);
        cout << "INTER_LANCZOS4: " << dst.size() << endl; // 列x行 [864 x 180]
        imshow("INTER_LANCZOS4", dst);

        waitKey(0);
    }
}
