//
//  day012.cpp
//  LearningOpenCV
//
//  Created by bingqiangzhou on 2021/2/1.
//

#include <stdio.h>

#include "toc.h"


using namespace cv;


/** Day012-视频读写
 VideoCapture 视频文件读取、摄像头读取、视频流读取
 VideoWriter 视频写出、文件保存、
 常用属性
 - CAP_PROP_FRAME_HEIGHT
 - CAP_PROP_FRAME_WIDTH
 - CAP_PROP_FRAME_COUNT
 - CAP_PROP_FPS
 不支持音频编码与解码保存，不是一个音视频处理的库！主要是分析与解析视频内容。保存文件最大支持单个文件为2G
 */
namespace Day012 {
    void mainFunction(){
        VideoCapture capture; // 初始化VideoCapture对象
        capture.open("./data/videos/video.avi"); // 打开视频文件，open(0)则打开摄像头(0是deviceID)
        if (!capture.isOpened()) { // 判断是否正确打开
            printf("cloud not read this video file...\n");
            return ;
        }

        // 常用参数
        int height = capture.get(CAP_PROP_FRAME_HEIGHT);
        int width = capture.get(CAP_PROP_FRAME_WIDTH);
        int frames = capture.get(CAP_PROP_FRAME_COUNT);
        int fps = capture.get(CAP_PROP_FPS);
        int fourcc = capture.get(CAP_PROP_FOURCC);
        printf("height: %d, width: %d, frames: %d, fps: %d, fourcc: %d\n", height, width, frames, fps, fourcc);

        // 读取video.avi文件，并保存到test.mp4
        // 初始化VideoWriter对象writer，
        // 其中fourcc参数是用于压缩视频帧的编解码器的4个字符代码，
        // fourcc设置为-1，可以弹出选择编解码器的对话框（第一次运行时可以使用-1，来确定本机存在哪些编解码器）
        // codec参考：https://www.fourcc.org/codecs.php
        // macOS 下可用的codec：https://gist.github.com/takuma7/44f9ecb028ff00e2132e
        VideoWriter writer("./data/videos/test.mp4", CAP_FFMPEG, VideoWriter::fourcc('m', 'p', '4', 'v'), fps, Size(height, width), true);

        Mat frame;
        while (capture.read(frame)) { // 循环读取视频帧
            imshow("VideoCapture read video file", frame); // 显示视频帧
            writer.write(frame);
            char c = waitKey(50); // 每隔50毫秒，对键盘按键事件监听
            if (c == 27) {  // 如果按下ESC键（acsii对应27），退出循环读取视频帧
                break;
            }
        }
        writer.release();
        capture.release(); // 释放VideoCapture资源

        
        // 使用摄像头录制视频
        // 在macOS下，Xcode中运行可能遇到权限不足的情况：报错如下：
        // [access] This app has crashed because it attempted to access privacy-sensitive data without a usage description.
        // The app‘s Info.plist must contain an NSCameraUsageDescription key with a string value explaining to the user how the app uses this data.
        // 两种方法解决：
        // 第一种：进入到Products文件夹中打开exec文件即会申请放开权限，允许即可。
        // 第二种：创建info.plist文件添加一下两个key，并复制到Products文件夹中（如果有clean项目的话，需要重新复制）
        // <key>NSCameraUsageDescription</key>
        // <string>USE</string>
        // <key>Privacy - Camera Usage Description</key>
        // <string>YES</string>
        // info.plist 在data/others文件夹下可以找到，直接复制到Products文件夹中即可
        
        VideoCapture camera_capture;
        camera_capture.open(0);
        if (!camera_capture.isOpened()) {
            printf("cloud not open camera...\n");
            return ;
        }
        
        VideoWriter camera_writer;
        camera_writer.open("./data/videos/camera.avi", CAP_FFMPEG, VideoWriter::fourcc('D', 'I', 'V', 'X'), 30, Size(500, 500), true);
        
        // Mat frame;
        while (true) {
            camera_capture.read(frame);
            imshow("i see you!", frame);
            camera_writer.write(frame);
            char c = waitKey(50); // 每隔50毫秒，对键盘按键事件监听
            if (c == 27) {  // 如果按下ESC键（acsii对应27），退出循环读取视频帧
                break;
            }
        }
        camera_writer.release();
        camera_capture.release();
    }
}
