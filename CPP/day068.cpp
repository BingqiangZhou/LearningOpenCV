#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <math.h>
using namespace cv;
using namespace std;
int main(int argc, char** argv)
{
	Mat dresult, eresult;
	Mat src = imread("D:/images/morph.png");

	// 二值图像
	Mat gray, binary, result;
	cvtColor(src, gray, COLOR_BGR2GRAY);
	threshold(gray, binary, 0, 255, THRESH_BINARY | THRESH_OTSU);
	imshow("binary", binary);

	// 定义结构元素
	Mat se = getStructuringElement(MORPH_RECT, Size(9, 9), Point(-1, -1));
	// 黑帽操作
	morphologyEx(binary, result, MORPH_BLACKHAT, se);

	// 显示
	imshow("tophat demo", result);
	waitKey(0);
	return 0;
}