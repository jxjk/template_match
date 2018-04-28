# -*- coding: utf-8 -*-
"""
p131  测试失败，占用资源过多
car_sliding_windows.py
测试模板匹配检测器
jxjk 20180404
"""
import cv2
import numpy as np 
#from car_detector.detector import car_detector,bow_features
from car_detector.pyramid import pyramid
from car_detector.non_maximum import non_max_suppression_fast as nms 
from car_detector.pyramid import sliding_window
from dataBase.access import *

def in_range(number,test,thresh = 0.2):
	return abs(number - test) < thresh


def nothing(x):
	pass


#test_image = r"C:\Users\00597\Pictures\images\zhouChen1.jpg" # path to cars.jpg
#temp_image = r"C:\Users\00597\Pictures\images\zhouChen2.jpg" # path to temp.jpg
test_image = r"C:\Users\00597\Pictures\images\zhouChen4.jpg" # path to cars.jpg
temp_image = r"C:\Users\00597\Pictures\images\zhouChen6.jpg" # path to temp.jpg
#test_image = r"C:\Users\00597\Documents\VimFile\mingshizong\imgs\src.jpg" # path to cars.jpg
#temp_image = r"C:\Users\00597\Documents\VimFile\mingshizong\imgs\template.jpg" # path to temp.jpg
# temp

型号 = "3"
pathfile = r'dataBase/test.mdb'
tablename = r'prov'
conn = mdb_conn(pathfile)
cur = conn.cursor()

#查
sql = "SELECT * FROM " + tablename + " where 型号 = " + 型号
sel_data = mdb_sel(cur, sql)
print(sel_data)

img1 = cv2.imread(temp_image,0)
cv2.namedWindow("image")

w,h = sel_data[0][1],sel_data[0][2]
print(w)
print(h)
cv2.createTrackbar('w','image',w,255,nothing)
cv2.createTrackbar('h','image',h,255,nothing)

#w,h = 90,96
#w,h = 52,58
#w,h = 58,63
while(1):
	
	w = cv2.getTrackbarPos('w','image')
	h = cv2.getTrackbarPos('h','image')
	#w,h = img1.shape[:2]

	img = cv2.imread(test_image)

	rectangles = []
	counter = 1
	scaleFactor =2#1.25
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
				img2 = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
			
				ret = cv2.matchTemplate(img2,img1,cv2.TM_CCOEFF_NORMED)
				'''
				for score1 in ret:
					for score in score1:
						print(score)
						print("*"*10)
						if score >= 0.8:
				
							rx,ry,rx2,ry2 = int(x*scale),int(y*scale),int((x+w)*scale),int((y+h)*scale)
							rectangles.append([rx,ry,rx2,ry2,abs(score)])
				'''
				threshold = 0.63
				# 3.这边是Python/Numpy的知识，后面解释
				loc = np.where(ret >= threshold)  # 匹配程度大于%80的坐标y,x
			
				#print(loc[::-1])
				#print(ret)
				for pt in zip(*loc[::-1]):  # *号表示可选参数
					rx,ry,rx2,ry2 = int(x*scale),int(y*scale),int((x+w)*scale),int((y+h)*scale)
					rectangles.append([rx,ry,rx2,ry2,(ret[pt[0],pt[1]])])
					#right_bottom = (pt[0] + w, pt[1] + h)
					#cv2.rectangle(img_rgb, pt, right_bottom, (0, 0, 255), 2)

			except:
				pass

			counter += 1

	windows = np.array(rectangles)
	boxes = nms(windows,1)

	#boxes1 = np.stack(boxes,0)
	#print (boxes)
	a = boxes.tolist()

	#a = [[1, 2, 3], [1, 2, 3], [2, 3, 4], [2, 3, 4], [2, 3, 5], [5, 6, 7]] 
	#a = [a[i] for i in range(len(a)) if a[i] not in a[:i]]

	#a = [[1, 2, 3], [1, 2, 3], [2, 3, 4], [2, 3, 4], [2, 3, 5], [5, 6, 7]] 
	c = [] 
	for i in a: 
		if i not in c: 
			c.append(i) 
	a = c 
	#print(a)


	for (x,y,x2,y2,score) in a:
		#print (x,y,x2,y2,score)
		cv2.rectangle(img,(int(x),int(y)),(int(x2),int(y2)),(0,0,255),1)
		cv2.putText(img,"%f"%score,(int(x),int(y)),font,1,(0,0,255))
	print(len(a))

	cv2.imshow("image",img)
	q = cv2.waitKey(50) & 0xff 
	if q == 27:


    	#改
		sql = "Update " + tablename + " Set 型号 = " + 型号 + ", w = " + str(w) + ", h = " + str(h) + " where 型号 = " + 型号 
		if mdb_modi(conn, cur, sql):
			print("修改成功！")
		else:
			print("修改失败！")

		break

