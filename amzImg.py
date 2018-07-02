#!/usr/bin/env python3
from amazon import amazon
import time
imgs = []
#读取txt中的需要获取的源数据
f = open("img.txt","r+")# 返回一个文件对象   
line = f.readline()# 调用文件的 readline()方法  
while line:
	if not (line == '\n'):
		imgs.append(line)
	line = f.readline()
f.close()
#print(imgs)

#进行图片爬取

for img in imgs:
	amazon.getdata(img)
	time.sleep(5)
