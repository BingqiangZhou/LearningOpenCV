#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <math.h>
using namespace cv;
using namespace std;
int main(int argc, char** argv)
{
	Mat dresult, eresult;
	Mat src = imread("D:/images/cross.png");

	// 二值图像
	Mat gray, binary, result;
	cvtColor(src, gray, COLOR_BGR2GRAY);
	threshold(gray, binary, 0, 255, THRESH_BINARY_INV | THRESH_OTSU);
	imshow("binary", binary);

	// 定义结构元素
	Mat se = getStructuringElement(MORPH_CROSS, Size(11, 11), Point(-1, -1));
	// 击中击不中
	morphologyEx(binary, result, MORPH_HITMISS, se);

	// 显示
	imshow("hit-and-miss demo", result);
	waitKey(0);
	return 0;
}