'''
Author       : Bingqiang Zhou
Date         : 2021-02-16 00:01:00
LastEditors  : Bingqiang Zhou
LastEditTime : 2021-02-16 00:52:35
Description  : 图像模板匹配
    模板匹配被称为最简单的模式识别方法、同时也被很多人认为是最没有用的模式识别方法。
    这里里面有很大的误区，就是模板匹配是工作条件限制比较严格，
    只有满足理论设置的条件以后，模板匹配才会比较好的开始工作，
    而且它不是基于特征的匹配，所以有很多弊端，但是不妨碍它成为入门级别模式识别的方法，
    通过它可以学习到很多相关的原理性内容，为后续学习打下良好的基础。

    基本思想
        将模板图像在目标图像上滑动逐一对比，通过统计的基本方法进行匹配，比如方差检验，相关性检验等方法来寻找最佳匹配。

    OpenCV中模板匹配的API为
    void cv::matchTemplate (
    InputArray image,
    InputArray templ,
    OutputArray result,
    int method,
    InputArray mask = noArray() 
    )		
    Python:
    result = cv.matchTemplate(	image, templ, method[, result[, mask]] )

    其中method表示模板匹配时候采用的计算像素相似程度的方法，常见有如下
    TM_SQDIFF = 0
    TM_SQDIFF_NORMED = 1
    平方不同与平方不同的归一化版本

    TM_CCORR = 2
    TM_CCORR_NORMED = 3
    相关性，值越大相关性越强，表示匹配程度越高。
    归一化版本值在0～1之间，1表示高度匹配，0表示完全不匹配

    TM_CCOEFF = 4
    TM_CCOEFF_NORMED = 5
    相关因子，值越大相关性越强，表示匹配程度越高。
    归一化版本值在0～1之间，1表示高度匹配，0表示完全不匹配

    参考：
        https://blog.csdn.net/qq_30815237/article/details/86812716
'''

import cv2 as cv
import numpy as np

search_image = cv.imread("../data/images/llk.jpg")
template_image = cv.imread("../data/images/llk_tpl.png")

dst = cv.matchTemplate(search_image, template_image, method=cv.TM_CCOEFF_NORMED)

# 可视化：将阈值大于t的位置画矩形框
th, tw = template_image.shape[:2]
t = 0.95 # 设置相关性阈值
y, x = np.where(dst > t) # (行，列)
search_result = search_image.copy()
for pt in zip(x, y):
    search_result = cv.rectangle(search_result, pt, (pt[0]+tw, pt[1]+th), (255, 0, 0))

# 可视化
rows = 1
cols = 4
images = [search_image, template_image, dst, search_result]
titles = ["search_image", "template_image", "matchTemplate", "search_result"]
for index, image in enumerate(images):
    cv.imshow(titles[index], image)

cv.waitKey(0)
