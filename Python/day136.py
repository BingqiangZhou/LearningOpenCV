'''
Author       : Bingqiang Zhou
Date         : 2021-09-04 00:51:21
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-04 00:52:29
Description  : OpenCV DNN解析网络输出结果
    多数时候DNN模块中深度学习网络的输出结果，可能是二维、三维、或者四维的，
    具体跟网络的结构有很大的关系，一般常见的图像分类网络，是一个1XN维的向量，通过reshape之后就很容易解析，
    解析代码如下：
    Mat flat = prob.reshape(1,1)
    Point maxLoc;
    minMaxLoc(flat, 0, 0, &maxLoc)
    int predict = maxLoc.x;

    如果是对象检测网络SSD/RCNN/Faster-RCNN网络，输出的是NX7的模式
    所以其解析方式如下：
    Mat detectionMat(out.size[2]， out.size[3], CV_32F, out.ptr<float>())
    就可以解析该结构！

    如果对象检测网络是基于Region的YOLO网络，则解析方式变为
    Mat scores = outs[i].row(j).colRange(5, outs[i].cols);
    前面五个为cx,cy,w, h, objectness

    如果模型网络是图像分割的网络，最后一层输出是3通道的图像对象，则解析方式为：
    Mat green(224, 224, CV_32F, blob.ptr<float>(0, 1)) // 表示绿色通道！

    以上是对OpenCV DNN各种网络模型输出解析方法的总结！
'''

## 无代码
