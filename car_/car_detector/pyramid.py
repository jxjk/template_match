# -*- coding: utf-8 -8-
'''
pyramid.py
p124
图像金字塔、滑动窗口
jxjk20180404
'''
import cv2


def resize(img,scaleFactor):
	return cv2.resize(img,(int(img.shape[1] * (1 / scaleFactor)),\
		int(img.shape[0] * (1 / scaleFactor))),interpolation = cv2.INTER_AREA)


def pyramid(image,scale = 1.5,minSize = (200,80)):
	yield image
	while True:
		image = resize(image , scale)
		if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
			break

		yield image


def sliding_window(image,stepSize,windowSize):
	for y in range(0,image.shape[0],stepSize):
		for x in range(0,image.shape[1],stepSize):
			yield (x,y,image[y:y + windowSize[1],x:x + windowSize[0]])


