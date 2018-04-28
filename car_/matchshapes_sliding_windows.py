# -*- coding: utf-8 -*-
"""
p131
car_sliding_windows.py
测试形状匹配检测器
jxjk 20180404
"""
import cv2
import numpy as np 
#from car_detector.detector import car_detector,bow_features
from car_detector.pyramid import pyramid
from car_detector.non_maximum import non_max_suppression_fast as nms 
from car_detector.pyramid import sliding_window


def in_range(number,test,thresh = 0.2):
	return abs(number - test) < thresh


test_image = r"C:\Users\00597\Pictures\images\zhouChen1.jpg" # path to cars.jpg
temp_image = r"C:\Users\00597\Pictures\images\zhouChen2.jpg" # path to temp.jpg
#test_image = r"C:\Users\00597\Documents\VimFile\mingshizong\imgs\src.jpg" # path to cars.jpg
#temp_image = r"C:\Users\00597\Documents\VimFile\mingshizong\imgs\template.jpg" # path to temp.jpg

# 寻找样本轮廓
img1 = cv2.imread(temp_image,0)
img3 = cv2.imread(test_image,0)

#ret,thresh = cv2.threshold(img1,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
ret,thresh = cv2.threshold(img1,150,255,cv2.THRESH_BINARY)
img1,contours,hierachy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnt1 = contours[0]
ret,thresh3 = cv2.threshold(img3,150,255,cv2.THRESH_BINARY)

w,h = 50,50
#w,h = img1.shape[:2]
img = cv2.imread(test_image,0)

rectangles = []
counter = 1
scaleFactor = 1.25
scale = 1
font = cv2.FONT_HERSHEY_PLAIN

#寻找roi轮廓并作形状比较，<0.1 填充矩形
for resized in pyramid(img,scaleFactor):
	scale = float(img.shape[1]) / float(resized.shape[1])
	for (x,y,roi) in sliding_window(resized,20,(w,h)):
		if roi.shape[1] != w or roi.shape[0] != h:
			continue

		try:
			'''
			'''
			img2 = roi
			#ret,thresh2 = cv2.threshold(img2,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
			ret,thresh2 = cv2.threshold(img2,150,255,cv2.THRESH_BINARY)
			#print(thresh2)
			img2,contours2,hierachy = cv2.findContours(thresh2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			cnt2 = contours2[0]

			score = cv2.matchShapes(cnt1,cnt2,1,0.0)
			#print(score)
		
			if score <= 0.1:
				rx,ry,rx2,ry2 = int(x*scale),int(y*scale),int((x+w)*scale),int((y+h)*scale)
				rectangles.append([rx,ry,rx2,ry2,abs(score)])
			
		except:
			pass

		counter += 1

windows = np.array(rectangles)
boxes = nms(windows,0.1)

for (x,y,x2,y2,score) in boxes:
	print (x,y,x2,y2,score)
	cv2.rectangle(img,(int(x),int(y)),(int(x2),int(y2)),(0,0,255),1)
	cv2.putText(img,"%f"%score,(int(x),int(y)),font,1,(0,0,255))

cv2.imshow("img",img)
cv2.imshow("thresh",thresh)
cv2.imshow("thresh3",thresh3)
cv2.waitKey(0)

