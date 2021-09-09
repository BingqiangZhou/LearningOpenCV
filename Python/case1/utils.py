'''
Author       : Bingqiang Zhou
Date         : 2021-09-08 19:33:07
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-09-09 00:18:36
Description  : 案例一 – 识别0～9印刷体数字
    基于二值图像分析， 通过提取字符的40个特征向量生成字符特征
    其中对每个字符的ROI区域，计算4x5的网格，对每个网络计算像素个数，然后生成20个特征向量。
    在这个过程中充分考虑到浮点数Cell大小与分割，采用基于权重的分割方法，实现网格分割。

    同时对ROI区域进行X-Project与Y-Project方向投影，每个投影直方图分为10个Bins，这样就得到了20个向量:

    分别对上述的结果进行0～1之间的归一化处理，得到最终的每个字符的40个特征向量表示。
    基于字符的特征向量，计算它们之间的L2距离，得到对应的预测结果。

    首先来看一下如何提取40个特征向量， 这个里面涉及到两个很关键的技巧，一个是浮点数权重、一个是归一化，
    浮点数权重是可以提升准确率，归一化在某些程度上是可以保证字符的放缩不变性。
'''

import numpy as np

def extract_feature(roi):
    
    features = []
    h_roi, w_roi = roi.shape[:2]

    ## 将roi切分为高宽为5x4的block，每一个block的高宽
    h_block, w_block = h_roi / 5., w_roi / 4.
    for y in np.linspace(0, h_roi, 5, endpoint=False):
        for x in np.linspace(0, w_roi, 4, endpoint=False):
            features.append(get_weight_block_value(roi, x, y, h_block, w_block))
    
    ## 将roi区域按x坐标切分为10个bins进行统计
    w_cells = w_roi / 10.
    for x in np.linspace(0, w_roi, 10, endpoint=False):
        features.append(get_weight_block_value(roi, x, 0, h_roi, w_cells))

    ## 将roi区域按y坐标切分为10个bins进行统计
    h_cells = h_roi / 10.
    for y in np.linspace(0, h_roi, 10, endpoint=False):
        features.append(get_weight_block_value(roi, 0, y, h_cells, w_roi))
    
    ## 分别归一化三部分特征值
    features = np.array(features)
    features[:20] = features[:20] / max(features[:20])
    features[20:30] = features[20:30] / max(features[20:30])
    features[30:] = features[30:] / max(features[30:])

    return features
      

def get_weight_block_value(roi, x, y, h_block, w_block):
    h_roi, w_roi = roi.shape[:2]

    # 获取block 右下角的坐标
    x_block, y_block = min(x+w_block, w_roi-1), min(y+h_block, h_roi-1)

    ## 取整，向外扩张为整数区域
    x_int, y_int = int(x), int(y)
    x_block_int, y_block_int = min(int(x_block)+1, w_roi-1), min(int(y_block)+1, h_roi-1)

    ## 统计向外扩张为整数区域中间整数块区域数值
    value = np.sum(roi[y_int:y_block_int, x_int:x_block_int] == 0)
    
    ## block 左边浮点数区域数值
    left_value = 0
    if x - x_int > 0:
        left_value = (x-x_int) * np.sum(roi[y_int:y_block_int+1, x_int] == 0)
    ## block 上方浮点数区域数值
    top_value = 0
    if y - y_int > 0:
        top_value = (y-y_int) * np.sum(roi[y_int, x_int:x_block_int+1] == 0)
    ## block 右边浮点数区域数值
    right_value = 0
    if x_block_int - x_block > 0:
        right_value = (x_block_int-x_block) * np.sum(roi[y_int:y_block_int+1, x_block_int] == 0)
    ## block 下方浮点数区域数值
    bottom_value = 0
    if y_block_int - y_block > 0:
        bottom_value = (y_block_int-y_block) * np.sum(roi[y_block_int, x_int:x_block_int+1] == 0)
    
    value = max(value - left_value - top_value - right_value - bottom_value, 0)

    return value


    
    


