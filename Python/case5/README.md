<!--
 * @Author       : Bingqiang Zhou
 * @Date         : 2021-09-11 00:24:01
 * @LastEditors  : Bingqiang Zhou
 * @LastEditTime : 2021-09-11 00:58:45
 * @Description  : 
-->

# 案例五 - 分水岭分割案例

基于分水岭对象分割实现计数的例子，算法的主要步骤可以拆解为如下：

1. 去噪声，这步要根据实际图像来选择高斯模糊、双边、均值迁移、非局部均值去噪声等方法
2. 灰度化与二值化，选择合适二值化方法也很重要
3. 距离变换 + 阈值处理
4. 寻找与标记marker
5. 根据marker实现图像分水岭分割
6. 根据marker生成颜色填充

分水岭分割官方教程：
    [Image Segmentation with Watershed Algorithm](https://docs.opencv.org/master/d3/db4/tutorial_py_watershed.html)

## 寻找与标记marker

- 方式一：找到轮廓，填充轮廓不同的值，见[app.py](./app.py)
- 方式二：使用形态学操作确认前背景像素以及不确定的像素，再用连通组件做标记，这种方法更加通用，见[官方教程](https://docs.opencv.org/master/d3/db4/tutorial_py_watershed.html)

这个过程将不同的独立的形状标记成不同的数字，0表示未知标记，1、2、……、n表示背景与前景。

经过分水岭分割之后，0将会被分配到前景与背景，另外，前景的边缘值被设置为-1。

## 根据marker生成颜色填充

### 获取colormap

```python
color_map = plt.get_cmap(color_map_name)
rgb_array = cm.get_cmap(color_map)(np.linspace(0, 1, num=color_map.N), bytes=True)[:, :3] # RGBA
```

参考：

- [Choosing Colormaps in Matplotlib](https://matplotlib.org/stable/tutorials/colors/colormaps.html)
- [utils.py](https://github.com/BingqiangZhou/Interactive-Multi-target-Segmentation/blob/master/demo/codes/utils.py)

### 颜色填充

```python
seg_image = rgb_array[markers]
```
