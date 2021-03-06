<!--
 * @Author       : Bingqiang Zhou
 * @Date         : 2021-01-24 18:15:02
 * @LastEditors  : Bingqiang Zhou
 * @LastEditTime : 2021-03-02 21:55:48
 * @Description  : 
-->

# 学习笔记目录

| Day | title | content | code |
| :---: | :---: | :---: | :---: |
| 001 | 图像读取与显示 | 读取图像 - imread</br>显示图像 - imshow | [C++](../../CPP/codes/day001.cpp) / [Python](../../Python/day001.py)
| 002 | 图像色彩空间转换 | 色彩空间转换函数- cvtColor</br>图像保存 - imwrite | [C++](../../CPP/codes/day002.cpp) / [Python](../../Python/day002.py)|
| 003 | 图像对象的创建与赋值 | C++中Mat对象与创建</br>Python中Numpy数组对象 | [C++](../../CPP/codes/day003.cpp) / [Python](../../Python/day003.py)|
| 004 | 图像像素的读写操作 | C++中的像素遍历与访问</br>Python中的像素遍历与访问 | [C++](../../CPP/codes/day004.cpp) / [Python](../../Python/day004.py)|
| 005 | 图像像素的算术操作 | 加 - add、减 - subtract、乘 - multiply、除 - divide</br>防止数据越界 - saturate_cast(C++) | [C++](../../CPP/codes/day005.cpp) / [Python](../../Python/day005.py)
| 006 | LUT(Look Up Table, 查找表)的作用与用法 | 查找表主要用途：颜色匹配、伪色彩增强</br>applyColorMap(src, dst, COLORMAP) | [C++](../../CPP/codes/day006.cpp) / [Python](../../Python/day006.py)|
| 007 | 图像像素的逻辑操作 | 与 - bitwise_and、或 - bitwise_or、异或 - bitwise_xor</br>非 - bitwise_not | [C++](../../CPP/codes/day007.cpp) / [Python](../../Python/day007.py)|
| 008 | 图像通道分离与合并 |  通道分类 - split、通道合并 - merge</br>混合通道 - mixChannels | [C++](../../CPP/codes/day008.cpp) / [Python](../../Python/day008.py) |
| 009 | 图像色彩空间转换 |  色彩空间转换 - cvtColor</br>提取指定色彩范围区域 - inRange | [C++](../../CPP/codes/day009.cpp) / [Python](../../Python/day009.py) |
| 010 | 图像像素值统计 |  最大最小值 - minMaxLoc</br>计算均值与标准方差 - meanStdDev | [C++](../../CPP/codes/day010.cpp) / [Python](../../Python/day010.py) |
| 011 | 像素归一化 |  像素归一化 - normalize</br>NORM_MINMAX、NORM_INF、NORM_L1、NORM_L2 | [C++](../../CPP/codes/day011.cpp) / [Python](../../Python/day011.py) |
| 012 | 视频文件的读写 |  视频文件读取、摄像头读取、视频流读取 - VideoCapture</br>视频写出、文件保存 - VideoWriter | [C++](../../CPP/codes/day012.cpp) / [Python](../../Python/day012.py) |
| 013 | 图像翻转(Image Flip) |  图像翻转 - flip</br>flipcode参数 - X轴翻转(0)、Y轴翻转(1)、 XY轴翻转(-1) | [C++](../../CPP/codes/day013.cpp) / [Python](../../Python/day013.py) |
| 014 | 图像插值(Image Interpolation) | 改变图像大小 - resize</br>INTER_NEAREST(0)、INTER_LINEAR(1) </br>  INTER_CUBIC(2)、INTER_LANCZOS4(4) | [C++](../../CPP/codes/day014.cpp) / [Python](../../Python/day014.py) |
| 015 | 几何形状绘制 | 绘制几何形状 - line、rectangle、circle、ellipse</br>随机数方法 - (c++)rng. 、(python)np.random. | [C++](../../CPP/codes/day015.cpp) / [Python](../../Python/day015.py) |
| 016 | 图像ROI与ROI操作 | ROI区域提取</br>ROI区域操作 | [C++](../../CPP/codes/day016.cpp) / [Python](../../Python/day016.py) |
| 017 | 图像直方图 | 计算图像直方图 - calcHist | [C++](../../CPP/codes/day017.cpp) / [Python](../../Python/day017.py) |
| 018 | 图像直方图均衡化 | 直方图均衡化 - equalizeHist | [C++](../../CPP/codes/day018.cpp) / [Python](../../Python/day018.py) |
| 019 | 图像直方图比较 | 图像直方图比较 - compareHist</br>比较方法 - 相关性、卡方、交叉、巴氏距离 | [C++](../../CPP/codes/day019.cpp) / [Python](../../Python/day019.py) |
| 020 | 图像直方图反向投影 | 图像直方图反向投影 - calcBackProject | [C++](../../CPP/codes/day020.cpp) / [Python](../../Python/day020.py) |
| 021 | 图像卷积操作 | 均值模糊 - blur</br>卷积核所有值为1 / (ksize.width * ksize.height) | [C++](../../CPP/codes/day021.cpp) / [Python](../../Python/day021.py) |
| 022 | 图像均值模糊与高斯模糊 | 均值模糊 - blur</br>高斯模糊 - GaussianBlur | [C++](../../CPP/codes/day022.cpp) / [Python](../../Python/day022.py) |
| 023 | 图像中值模糊 | 中值模糊 - medianBlur | [C++](../../CPP/codes/day023.cpp) / [Python](../../Python/day023.py) |
| 024 | 图像噪声 | 图像椒盐噪声</br>图像高斯噪声 | [C++](../../CPP/codes/day024.cpp) / [Python](../../Python/day024.py) |
| 025 | 图像去噪声 | 均值去噪声 - blur、中值去噪声 - medianBlur</br>高斯模糊去噪声 - GaussianBlur</br>非局部均值去噪声 - fastNlMeansDenoisingColored | [C++](../../CPP/codes/day025.cpp) / [Python](../../Python/day025.py) |
| 026 | 高斯双边模糊 | 高斯双边模糊 - bilateralFilter | [C++](../../CPP/codes/day026.cpp) / [Python](../../Python/day026.py) |
| 027 | 均值迁移模糊 | 均值迁移模糊 - pyrMeanShiftFiltering | [C++](../../CPP/codes/day027.cpp) / [Python](../../Python/day027.py) |
| 028 | 图像积分图算法 | 图像积分图 - integral | [C++](../../CPP/codes/day028.cpp) / [Python](../../Python/day028.py) |
| 029 | 快速的图像边缘滤波算法 | 快速的图像边缘滤波 - edgePreservingFilter | [C++](../../CPP/codes/day029.cpp) / [Python](../../Python/day029.py) |
| 030 | OpenCV自定义的滤波器 | 自定义滤波器 - filter2D</br>缩放，绝对值，转换为8位 - convertScaleAbs | [C++](../../CPP/codes/day030.cpp) / [Python](../../Python/day030.py) |
| 031 | 图像梯度–Sobel算子 | Sobel算子</br>Scharr算子 | [C++](../../CPP/codes/day031.cpp) / [Python](../../Python/day031.py) |
| 032 | 图像梯度–更多梯度算子 | Robert算子</br>Prewitt算子 | [C++](../../CPP/codes/day032.cpp) / [Python](../../Python/day032.py) |
| 033 | 图像梯度–拉普拉斯算子 | 拉普拉斯算子 - 四邻域、八邻域 | [C++](../../CPP/codes/day033.cpp) / [Python](../../Python/day033.py) |
| 034 | 图像锐化 | 锐化的本质是拉普拉斯滤波与原图权重像素叠加 | [C++](../../CPP/codes/day034.cpp) / [Python](../../Python/day034.py) |
| 035 | USM锐化增强算法 | USM(Unsharpen Mask)锐化增强算法</br>权重叠加 - addWeighted | [C++](../../CPP/codes/day035.cpp) / [Python](../../Python/day035.py) |
| 036 | Canny边缘检测器 | Canny边缘检测器 - Canny | [C++](../../CPP/codes/day036.cpp) / [Python](../../Python/day036.py) |
| 037 | 图像金字塔 | reduce操作 - pyrDown</br>expand操作 - pyrUp | [C++](../../CPP/codes/day037.cpp) / [Python](../../Python/day037.py) |
| 038 | 拉普拉斯金字塔 | 高斯金字塔</br>拉普拉斯金字塔 | [C++](../../CPP/codes/day038.cpp) / [Python](../../Python/day038.py) |
| 039 | 图像模板匹配 | 图像模板匹配 - matchTemplate | [C++](../../CPP/codes/day039.cpp) / [Python](../../Python/day039.py) |
| 040 | 二值图像介绍 | 二值图像 - 0表示黑色、1表示白色(255)</br>二值分割  | [C++](../../CPP/codes/day040.cpp) / [Python](../../Python/day040.py) |
| 041 | OpenCV中的基本阈值操作 | 阈值操作 - threshold</br>THRESH_BINARY、THRESH_BINARY_INV</br>THRESH_TRUNC</br>THRESH_TOZERO、THRESH_TOZERO_INV | [C++](../../CPP/codes/day041.cpp) / [Python](../../Python/day041.py) |
| 042 | OTSU二值寻找算法 | 阈值操作 - threshold</br>THRESH_OTSU | [C++](../../CPP/codes/day042.cpp) / [Python](../../Python/day042.py) |
| 043 | TRIANGLE二值寻找算法 | 阈值操作 - threshold</br>THRESH_TRIANGLE | [C++](../../CPP/codes/day043.cpp) / [Python](../../Python/day043.py) |
| 044 | 自适应阈值算法 | 自适应阈值算法 - adaptiveThreshold</br>ADAPTIVE_THRESH_GAUSSIAN_C</br>ADAPTIVE_THRESH_MEAN_C | [C++](../../CPP/codes/day044.cpp) / [Python](../../Python/day044.py) |
| 045 | 图像二值化与去噪 | 先去噪声后二值化 | [C++](../../CPP/codes/day045.cpp) / [Python](../../Python/day045.py) |
| 046 | 二值图像联通组件寻找 | 连通组件标记算法 - connectedComponents | [C++](../../CPP/codes/day046.cpp) / [Python](../../Python/day046.py) |
| 047 | 二值图像连通组件状态统计 | 带统计信息的连通组件查找</br>connectedComponentsWithStats | [C++](../../CPP/codes/day047.cpp) / [Python](../../Python/day047.py) |
| 048 | 二值图像分析-轮廓发现 | 轮廓发现 - findContours</br>绘制轮廓 - drawContours | C++ / [Python](../../Python/day048.py) |
| 049 | 二值图像分析-轮廓外接矩形 | 最大外接轮廓矩形 - boundingRect</br>最小外接矩形 - minAreaRect | C++ / [Python](../../Python/day049.py) |
| 050 | 二值图像分析-矩形面积与弧长 | 轮廓面积 - contourArea</br>弧长 - arcLength | C++ / [Python](../../Python/day050.py) |
| 051 | 二值图像分析-使用轮廓逼近 | 轮廓逼近 - approxPolyDP | C++ / [Python](../../Python/day051.py) |
| 052 | 二值图像分析-用几何矩计算轮廓中心与横纵比过滤 | 计算几何距 - moments | C++ / [Python](../../Python/day052.py) |
| 053 | 二值图像分析-Hu矩实现轮廓匹配 | 计算Hu距 - HuMoments</br>轮廓外形匹配 - matchShapes | C++ / [Python](../../Python/day053.py) |
| 054 | 二值图像分析—对轮廓圆与椭圆拟合 | 拟合椭圆或者圆形 - fitEllipse | C++ / [Python](../../Python/day054.py) |
| 055 | 二值图像分析-凸包检测 | 对轮廓提取凸包 - convexHull</br>判断轮廓是否为凸包 - isContourConvex | C++ / [Python](../../Python/day055.py) |
| 056 | 二值图像分析-直线拟合与极值点寻找 | 直线拟合 - fitLine | C++ / [Python](../../Python/day056.py) |
| 057 | 二值图像分析-点多边形测试 | 点多边形测试 - pointPolygonTest | C++ / [Python](../../Python/day057.py) |
| 058 | 二值图像分析-寻找最大内接圆 | 通过点多边形测试巧妙的获取轮廓最大内接圆的半径 | C++ / [Python](../../Python/day058.py) |
| 059 | 二值图像分析-霍夫直线检测（一） | 霍夫直线检测 - HoughLines | C++ / [Python](../../Python/day059.py) |
| 060 | 二值图像分析-霍夫直线检测（二） | 霍夫直线检测 - HoughLinesP | C++ / [Python](../../Python/day060.py) |
| 061 | 二值图像分析-霍夫圆检测 | 霍夫圆检测 - HoughCircles | C++ / [Python](../../Python/day061.py) |
| 062 | 图像形态学-膨胀与腐蚀（一） | 膨胀 - dilate</br>腐蚀 - erode | C++ / [Python](../../Python/day062.py) |
| 063 | 图像形态学-膨胀与腐蚀（二） | 获取结构元素 - getStructuringElement | C++ / [Python](../../Python/day063.py) |
| 064 | 图像形态学-开操作 | 形态学转换 - morphologyEx</br>开操作 - MORPH_OPEN</br>开操作 = 腐蚀 + 膨胀 | C++ / [Python](../../Python/day064.py) |
| 065 | 图像形态学-闭操作 | 形态学转换 - morphologyEx</br>闭操作 - MORPH_CLOSE</br>开操作 = 膨胀 + 腐蚀 | C++ / [Python](../../Python/day065.py) |
| 066 | 图像形态学-开闭操作时候结构元素应用演示 | 开操作提取水平线，实现填空题横线位置提取</br>闭操作实现不同层次的轮廓填充 | C++ / [Python](../../Python/day066.py) |
| 067 | 图像形态学-顶帽操作 | 形态学转换 - morphologyEx</br>顶帽操作 - MORPH_TOPHAT</br>顶帽 = 输入图像 - 开操作 | C++ / [Python](../../Python/day067.py) |
| 068 | 图像形态学-黑帽操作 | 形态学转换 - morphologyEx</br>黑帽操作 - MORPH_BLACKHAT</br>黑帽操作 = 闭操作 - 输入图像 | C++ / [Python](../../Python/day068.py) |
| 069 | 图像形态学-图像梯度 | 形态学转换 - morphologyEx</br>基本梯度 - MORPH_GRADIEN</br>基本梯度 = 膨胀操作 - 腐蚀操作</br>内梯度 = 输入图像- 腐蚀操作</br>外梯度 = 膨胀操作 - 输入图像 | C++ / [Python](../../Python/day069.py) |
| 070 | 形态学应用-用基本梯度实现轮廓分析 | 用基本梯度实现轮廓分析 | C++ / [Python](../../Python/day70.py) |
| 071 | 形态学应用-击中击不中 | 形态学转换 - morphologyEx</br>击中击不中操作 - MORPH_HITMISS | C++ / [Python](../../Python/day71.py) |
| 072 | 二值图像分析案例 | 缺陷检测一 - 提取指定的轮廓 | C++ / [Python](../../Python/day72.py) |
| 073 | 二值图像分析案例 | 缺陷检测二 - 实现缺陷检测 | C++ / [Python](../../Python/day73.py) |
| 074 | 二值图像分析案例 | 提取最大轮廓与编码关键点 - 提取星云的区域 | C++ / [Python](../../Python/day74.py) |
| 075 | 图像去水印/修复 | 图像修复 - inpaint | C++ / [Python](../../Python/day75.py) |
| 076 | 图像透视变换应用 | 图像透视变换应用 - warpPerspective</br>获取透视变换矩阵 - getPerspectiveTransform</br>获取透视变换矩阵 - findHomography | C++ / [Python](../../Python/day76.py) |
| 077 | 视频读写与处理 | 视频读写与处理 - VideoCapture | C++ / [Python](../../Python/day77.py) |
| 078 | 识别与跟踪视频中的特定颜色对象 | 色彩转换BGR2HSV</br>inRange提取颜色区域mask</br>对mask区域进行二值分析得到位置与轮廓信息</br>绘制外接椭圆与中心位置 | C++ / [Python](../../Python/day78.py) |
| 079 | 视频分析-背景/前景提取（运动分析） | 基于高斯混合模型GMM- createBackgroundSubtractorMOG2</br>基于最近邻KNN - createBackgroundSubtractorKNN | C++ / [Python](../../Python/day79.py) |
| 080 | 视频分析-背景消除与前景ROI提取 | 初始化背景建模对象GMM</br>读取视频一帧</br>使用背景建模消除生成mask</br>对mask进行轮廓分析提取ROI | C++ / [Python](../../Python/day80.py) |
