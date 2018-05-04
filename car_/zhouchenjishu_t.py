# --* coding: utf-8 *--
import cv2
import os
import numpy as np 
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import imutils
import time
from car_detector.pyramid import pyramid
from car_detector.non_maximum import non_max_suppression_fast as nms 
from car_detector.pyramid import sliding_window
from dataBase.access import *
from tkinter.messagebox import *
from PIL import Image
from PIL import ImageTk
import mysql.connector



def test():
    config = {'host':'127.0.0.1',
            'user':'root',
            'password':'abcd@1234',
            'port':'3306',
            'database':'test',
            'charset':'utf8'
            }
    #型号 = '12' 
    型号 = v4.get()
    print(型号)
    try:
        conn = mysql.connector.Connect(**config)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))

    cursor = conn.cursor()
#查
    try:
        sql = "SELECT * FROM  prov WHERE XH = %s" 
        cursor.execute(sql,(型号,))
        sel_data = cursor.fetchone()
        print(sel_data)
    except mysql.connector.Error as e:
        print('query error!{}'.format(e))
    finally:
        cursor.close()
        conn.close()

    if sel_data:
        print('正确')
        global img
        img = Image.open(r"./imgs/" + v4.get() + 'temp.jpg')
        img = ImageTk.PhotoImage(img)
        #img = tk.PhotoImage(file = r"./imgs/" + v4.get() + 'temp.gif')
        tuPian.configure(image=img)
        XH.configure(bg = 'blue')
        return True
    else:
        print('错误')
        img = Image.open(r"./imgs/temp.jpg")
        img = ImageTk.PhotoImage(img)
        tuPian.configure(image=img)
        XH.configure(bg = 'red')
        return False


def test1():
    print('又错了')
    return True


def in_range(number,test,thresh = 0.2):
    return abs(number - test) < thresh


def nothing(x):
    pass


def login_1():
    # cap = cv2.VideoCapture('http://192.168.1.104:8080/shot.jpg')
    型号 = v4.get()
    pathfile = r'dataBase/test.mdb'
    tablename = r'prov'
    conn = mdb_conn(pathfile)
    cur = conn.cursor()

#查
    sql = "SELECT * FROM " + tablename + " where 型号 = '" + 型号 +"'"
    sel_data = mdb_sel(cur, sql)

    cv2.namedWindow('temp')
    try:
        w,h = sel_data[0][1],sel_data[0][2]
    except:
        w = 50
        h = 50
        
    cv2.createTrackbar('w','temp',w,255,nothing)
    cv2.createTrackbar('h','temp',h,255,nothing)
    
    cap = cv2.VideoCapture(1)
    #相机亮度、对比度、饱和度调整
    #cap.set(10,150)
    #cap.set(15,-1)
    #cap.set(11,16)
    #print(cap.get(11))16.0

    while (1):
        w = cv2.getTrackbarPos('w','temp')
        h = cv2.getTrackbarPos('h','temp')
        ret,image = cap.read()
        image = cv2.resize(image,(800,600),interpolation = cv2.INTER_CUBIC)
        
        cv2.rectangle(image,(150,100),(150+w+2,100+h+2),(0,255,0),1)
        cv2.imshow('temp',image) 
        k = cv2.waitKey(30) & 0xff
        print(k)
        if k == 13:# Enter

            #增
            sql = "Insert Into " + tablename + " Values ('"+ 型号 +"', " + str(w) +", " + str(h)  + ", 69" +")"
            print(sql)
            if mdb_add(conn, cur, sql):
                print("插入成功！")
            else:
                print("插入失败！")
                #改
                sql = "Update " + tablename + " Set 型号 = '" + 型号 + "', w = " + str(w) + ", h = " + str(h) + " where 型号 = '" + 型号 + "'" 
                if mdb_modi(conn, cur, sql):
                    print("修改成功！")
                else:
                    print("修改失败！")
            cur.close()    #关闭游标
            conn.close()   #关闭数据库连接
            break

    roi = image[101:101+h,151:151+w]
    
    cv2.imwrite(r"./imgs/" + v4.get() + 'temp.jpg',roi)

    print("login")
    cv2.destroyAllWindows()
    cap.release()

def add_1():
    if lbzsl.get() == '':
        v1.set('0')
    if lbdql.get() == '':
        v2.set('0')

    result = int(lbzsl.get()) + int(lbdql.get())
    v1.set(result)
    v2.set('0')
    #print('add')


def clear_():
    v1.set('0')
    v2.set('0')


def count_1():
    #global ret
    # cap = cv2.VideoCapture('http://192.168.1.104:8080/shot.jpg')
    
    型号 = v4.get()

    reta = os.path.isfile(r"./imgs/" + 型号 + 'temp.jpg')
    if not reta: 
        a = showinfo(title="样本确认", message="没有样本，请先登录！")
        cv2.destroyAllWindows()
        return()
    
    img1 = cv2.imread(r"./imgs/" + 型号 + 'temp.jpg',0)
    
    pathfile = r'dataBase/test.mdb'
    tablename = r'prov'
    conn = mdb_conn(pathfile)
    cur = conn.cursor()

#查
    sql = "SELECT * FROM " + tablename + " where 型号 = '" + 型号 +"'"
    sel_data = mdb_sel(cur, sql)

    cv2.namedWindow("image")
    try:
        w,h,threshold = sel_data[0][1],sel_data[0][2],sel_data[0][3]
    except:
        w = img1.shape[1]
        h = img1.shape[0]
        threshold = 69#0.78#0.80 #0.63
    if w < img1.shape[1] or  h < img1.shape[0]:
        w = img1.shape[1]
        h = img1.shape[0]
        threshold = 69#0.78#0.80 #0.63

        
    cv2.createTrackbar('w','image',w,255,nothing)
    cv2.createTrackbar('h','image',h,255,nothing)
    cv2.createTrackbar('threshold','image',threshold,100,nothing)

    cap = cv2.VideoCapture(1)
    i=0
    while(1):
        ret,image1 = cap.read()
        i += 1
        if i == 10:
            break
    cap.release()

    while(1):
            
        w = cv2.getTrackbarPos('w','image')
        h = cv2.getTrackbarPos('h','image')
        threshold = cv2.getTrackbarPos('threshold','image')/100

        if img1.shape[1] > 1.1*w or img1.shape[0] > 1.1*h:
            a = showinfo(title="w|h确认", message="w|h数值过小，请再试一次！")
            cv2.destroyAllWindows()
            break
        
        img = cv2.resize(image1,(800,600),interpolation = cv2.INTER_CUBIC)

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
                    #print("here")
                    continue

                try:

                    img2 = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
                    ret = cv2.matchTemplate(img2,img1,cv2.TM_CCOEFF_NORMED)
                    # 3.这边是Python/Numpy的知识，后面解释
                    loc = np.where(ret >= threshold)  # 匹配程度大于%80的坐标y,x
                            
                    for pt in zip(*loc[::-1]):  # *号表示可选参数
                        rx,ry,rx2,ry2 = int(x*scale),int(y*scale),int((x+w)*scale),int((y+h)*scale)
                        rectangles.append([rx,ry,rx2,ry2,(ret[pt[0],pt[1]])])

                except:
                    pass
                
                counter += 1

        windows = np.array(rectangles)

        boxes = nms(windows,1)
        if len(boxes) > 0:
            a = boxes.tolist()
            c = [] 
            for i in a: 
                if i not in c: 
                    c.append(i) 
            a = c
        else:
            a = [] 

        for (x,y,x2,y2,score) in a:
            cv2.rectangle(img,(int(x),int(y)),(int(x2),int(y2)),(0,0,255),1)
            cv2.putText(img,"%f"%score,(int(x),int(y)),font,1,(0,0,255))
        v2.set(len(a))

        cv2.imshow("image",img)
        q = cv2.waitKey(50) & 0xff 
        if q == 13: # Enter

            #增
            sql = "Insert Into " + tablename + " Values ('"+ 型号 +"', " + str(w) +", " + str(h)  + ", " + str(threshold*100) +")"
            print(sql)
            if mdb_add(conn, cur, sql):
                print("插入成功！")
            else:
                print("插入失败！")
                #改
                sql = "Update " + tablename + " Set 型号 = '" + 型号 + "', w = " + str(w) + ", threshold = " + str(threshold*100) + ", h = " + str(h) + " where 型号 = '" + 型号 + "'" 
                if mdb_modi(conn, cur, sql):
                    print("修改成功！")
                else:
                    print("修改失败！")
            cur.close()    #关闭游标
            conn.close()   #关闭数据库连接
            break
    cv2.destroyAllWindows()


def zhaoHe_():
    pass


def chaXun_():
    XH.configure(bg = 'blue')
    pass


root = tk.Tk()

v1 = tk.StringVar()
v2 = tk.StringVar()	
v3 = tk.StringVar()
v4 = tk.StringVar()
v5 = tk.StringVar() # ID_NO
v6 = tk.StringVar() # shuRu_NO
#v4.set("test")
#v3.set("30")
#v4.set("ELATD8-P9-B10")
#v5.set("000105138955")
#v6.set("000105138955#31000002237-20")

ft = tkFont.Font(family = 'Fixdsys',size = 18,weight = tkFont.BOLD)
ft20 = tkFont.Font(family = 'Fixdsys',size = 21,weight = tkFont.BOLD)
ft12 = tkFont.Font(family = 'Fixdsys',size = 12,weight = tkFont.BOLD)

root.title('轴承计数')
root.geometry('960x600')


tuPian = tk.Button(root,text = 'temp',width=50,height=50)
tuPian.place(x=10, y=10, width=100, height=162)#.pack(side=tk.TOP,padx =5,pady=5)

countFm = tk.LabelFrame(root)
countFm.place(x=110, y=10, width=840, height=162)#.pack(side=tk.RIGHT,padx = 10 ,pady =10)#,fill = "x"

ID_lb = tk.Label(countFm,text = '订单|指示书编号:',font = ft,anchor = tk.NW)
ID_lb.grid(row = 0,column= 1)

ID_NO = tk.Entry(countFm,textvariable = v5,font = ft)  
ID_NO.grid(row = 0 ,column= 2)

xinghao = tk.Label(countFm,text = '型号:',font = ft,anchor = tk.NW)  
xinghao.grid(row = 1 ,column= 0)

XH = tk.Entry(countFm,textvariable = v4,validate='key',validatecommand=test,invalidcommand=test1,font = ft)# 'focusout'
XH.grid(row = 1 ,column= 1)

IDShuLiang_lb = tk.Label(countFm,text = '订单|指示书数量:',font = ft,anchor = tk.NW)
IDShuLiang_lb.grid(row = 1,column= 2,padx =5,pady=5)

IDShuLiang_NO = tk.Label(countFm,textvariable = v3,font = ft,anchor = tk.NW)  
IDShuLiang_NO.grid(row = 1 ,column= 3,padx =5,pady=5)


count1 = tk.Button(countFm,text = '检测(数量：)',font = ft,command = count_1)
count1.grid(row = 2,column= 0,padx =5,pady=5)

lbdql = tk.Entry(countFm,textvariable = v2,font = ft)
lbdql.grid(row = 2,column= 1,padx =5,pady=5)

add1 = tk.Button(countFm,text = '累计(数量：)',font = ft,command = add_1)
add1.grid(row = 2,column= 2,padx =5,pady=5)

lbzsl = tk.Entry(countFm,textvariable = v1,width = 4,font = ft)
lbzsl.grid(row = 2,column= 3,padx =5,pady=5)

lbfm = tk.LabelFrame(root)
lbfm.place(x=10, y=182, width=940, height=68)#.pack(padx =10,pady = 10,fill = "x")

qingLing_bt = tk.Button(lbfm,text = '清零',width = 10,font = ft20,command = clear_)
qingLing_bt.grid(row = 0,column= 0,padx =16,pady=5)

login1_bt = tk.Button(lbfm,text = '登陆',width = 10,font = ft20,command = login_1)
login1_bt.grid(row = 0,column= 1,padx =12,pady=5)

zhaoHe_bt = tk.Button(lbfm,text = '照合',width = 10,font = ft20,command = zhaoHe_)
zhaoHe_bt.grid(row = 0,column= 2,padx =12,pady=5)

chaXun_bt = tk.Button(lbfm,text = '查询',width = 10,font = ft20,command = chaXun_)
chaXun_bt.grid(row = 0,column= 3,padx =12,pady=5)

quit1 = tk.Button(lbfm,text = '退出',width = 10,font = ft20,command = root.quit)
quit1.grid(row = 0,column= 5,padx =12,pady=5)


shuRu_lb = tk.Label(root,text = "读取指示书&型号二维码：",font = ft12)  
shuRu_lb.place(x=10, y=270, width=200, height=20)#.pack(padx =10,pady = 0)

shuRu_NO = tk.Entry(root,textvariable = v6,font = ft12)
shuRu_NO.focus_set()
shuRu_NO.place(x=210, y=270, width=730, height=20)#.pack(padx =10,pady = 0,fill = "x",)

#使用Treeview组件实现表格功能

frame = tk.Frame(root)

frame.place(x=10, y=300, width=940, height=280)

#滚动条

scrollBar = tk.Scrollbar(frame)

scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

#Treeview组件，6列，显示表头，带垂直滚动条

tree = ttk.Treeview(frame,columns=('c1', 'c2', 'c3','c4', 'c5', 'c6'),show="headings",yscrollcommand=scrollBar.set)

#设置每列宽度和对齐方式

tree.column('c1', width=40, anchor='center')

tree.column('c2', width=200, anchor='center')

tree.column('c3', width=200, anchor='center')

tree.column('c4', width=120, anchor='center')

tree.column('c5', width=100, anchor='center')

tree.column('c6', width=280, anchor='center')

#设置每列表头标题文本

tree.heading('c1', text='ID')

tree.heading('c2', text='订单|指示书编号')

tree.heading('c3', text='产品型号')

tree.heading('c4', text='数量')

tree.heading('c5', text='记录时间')

tree.heading('c6', text='图片位置')

tree.pack(side=tk.LEFT, fill=tk.Y)

#Treeview组件与垂直滚动条结合

scrollBar.config(command=tree.yview)

#定义并绑定Treeview组件的鼠标单击事件

def treeviewClick(event):

    pass

tree.bind('<Button-1>', treeviewClick)



#插入演示数据
def tree_data(values=[]):
    for i in range(len(values)):
        tree.insert('', i, values=values[i])


val = [["1","000105138955","ELATD8-P9-B10","10","2018.5.2 10:10","./IMGS/000105138955_1.jpg"],["2","000105138955","ELATD8-P9-B10","20","2018.5.2 10:10","./IMGS/000105138955_2.jpg"]]
tree_data(val)

#运行程序，启动事件循环

root.mainloop()



