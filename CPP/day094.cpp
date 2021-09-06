#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main(int argc, char** argv) {
	Mat src = imread("D:/images/grad.png");
	auto orb_detector = ORB::create(1000);
	vector<KeyPoint> kpts;
	orb_detector->detect(src, kpts);
	Mat result = src.clone();
	drawKeypoints(src, kpts, result, Scalar::all(-1), DrawMatchesFlags::DEFAULT);
	imshow("ORB-detector", result);
	imwrite("D:/result.png", result);
	waitKey(0);
	return 0;
}
