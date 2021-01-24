<!--
 * @Author       : Bingqiang Zhou
 * @Date         : 2021-01-24 17:47:45
 * @LastEditors  : Bingqiang Zhou
 * @LastEditTime : 2021-01-24 17:56:26
 * @Description  : 
-->

# 配置环境

## OpenCV C++环境配置

- Mac
  - 安装 Homebrew

    参考：[Homebrew / Linuxbrew 镜像使用帮助](https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/)

  - 安装xcode

    ```bash
    brew install opencv
    ```

  - 项目配置
    - 安装 Homebrew

    参考：[Homebrew / Linuxbrew 镜像使用帮助](https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/)

  - 安装xcode

    ```bash
    brew install opencv
    ```

  - 项目配置
  
    - 在xocde中建立一个Command Line Tool工程，选择C++语言。
    - 左键点击项目目录顶层的配置文件，找到Build Settings中的Search Path栏目下的Header Search Paths，将下载好的头文件路径/usr/local/Cellar/opencv/4.x.x/include/opencv4/添加到这里。
    - 继续找到配置文件General中的Linked Frameworks and Libraries栏目，添加全部/usr/local/Cellar/opencv/4.x.x/lib路径下的.ylib结尾的文件。
    - 打开终端，通过pkg-config命令获取opencv所有的Linker Flags。

        ```bash
        pkg-config --cflags --libs opencv4
        ```

    - 选择Building Settings -> Other Linker Flags，将上面命令输出的结果添加到Linker Flags。

    (注意自己下载的版本，替换路径)

    参考：[Xcode上配置OpenCV和C++开发环境](https://gy23333.github.io/2020/01/16/Xcode上配置OpenCV和C-开发环境/)
  
  - 实际配置中遇过到的问题：
    
    .dyld库需要签名，报错: dyld: Library not loaded:XXXX......Reason: no suitable image found......[只需要将Signing&Capabilities中的Disalbe Library Validation点上即可。](https://github.com/opencv/opencv/issues/15645)


- Windows

    视频资料：[OpenCV4.0安装与环境配置-基于VS2015/VS2017 + Win10/Win7 64位](https://www.bilibili.com/video/BV1Dt411C79M)

## OpenCV Python环境配置

- 安装python
  
  参考：[安装Python](https://www.liaoxuefeng.com/wiki/1016959663602400/1016959856222624)

- 安装opencv-python包

  安装opencv-python或者opencv-contrib-python即可，opencv-contrib-python包括了额外的一些模块。

  >Packages for standard desktop environments (Windows, macOS, almost any GNU/Linux distribution)
  >
  >Option 1 - Main modules package: 
  >
  >```python
  >pip install opencv-python
  >```
  >
  >Option 2 - Full package (contains both main modules and contrib/extra modules): 
  >
  >```python
  >pip install opencv-contrib-python 
  >```
  >
  >(check contrib/extra modules listing from [OpenCV documentation](https://docs.opencv.org/master/))

视频资料：[OpenCV 4.0+Python3.6开发环境搭建](https://www.bilibili.com/video/BV1pb411C7VP)
