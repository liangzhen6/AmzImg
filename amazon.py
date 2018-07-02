#!/usr/bin/env python3
from download import request
from bs4 import BeautifulSoup
import os
import re
import json
import hashlib

class Amazon(object):
	"""docstring for Amazon"""

	def __init__(self):
		super(Amazon, self).__init__()
		self.img_urls = []#所有图片的url地址
		self.currentPath = os.path.abspath('.')

	def getdata(self,url):
		#清空数组
		self.img_urls.clear()
		#进入到根目录下
		os.chdir(self.currentPath)
		# headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
		html = request.get(url = url, timeout = 5)
		content_soup = BeautifulSoup(html.text, 'lxml')
		div = content_soup.find('div', id = 'imageBlock_feature_div')
		script = div.find_all('script')
		last = script[-1].string


		# resp = re.findall(r"{\"hiRes\":\"(.+?)\"",last)
		resp = re.findall(r"\'initial\': (.+?)}]}",last)
		jsonStr = resp[0] + '}]'
		jsonDict = json.loads(jsonStr)
		print(jsonDict)
		for dic in jsonDict:
			if dic['hiRes'] == None:
				imgArr = tuple(dic['main'].keys())
				lastImg = imgArr[-1]
				self.wirteUrl(lastImg)
				self.img_urls.append(lastImg)
				# print(tuple(dic.keys()))
			else:
				self.wirteUrl(dic['hiRes'])
				self.img_urls.append(dic['hiRes'])
		self.wirteUrl('\n\n\n')

		#创建文件夹
		path = self.genearteMD5(url)
		self.mkdir(path)

		#写入图片
		for img in self.img_urls:
			self.save_img(img)

		# print(jsonStr)
		# for img in resp:
		# 	self.wirteUrl(img)
		# self.wirteUrl('\n\n\n')


		# print(matchObj.group())
		# res = re.search(r'colorImages', script, re.M|re.I)
		# print(res.group())
		# all_ul = content_soup.find('ul', class_ = 'a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-extra-large')
		# all_li = all_ul.find_all('li', class_ = 'a-spacing-small item')
		# for i in range(len(all_li)):
		# 	li = all_li[i]
		# 	img = li.find('img')['src']
		# 	self.img_urls.append(img)
		# 	self.wirteUrl(img)
		# self.wirteUrl('\n\n\n')

	def wirteUrl(self,url):
		fp = open('amazon.txt','a')
		fp.write(url)
		fp.write('\n')
		fp.close()


	def mkdir(self,path):
		path = path.strip()
		# mypath = self.currentPath
		mypath = os.path.join(self.currentPath,'image')
		isExists = os.path.exists(os.path.join(mypath,path))
		if not isExists:
			os.makedirs(os.path.join(mypath,path))
			os.chdir(os.path.join(mypath,path))
			return True
		else:
			os.chdir(os.path.join(mypath,path))
			return False

	def save_img(self, image_url):
			name = image_url.split('/I/')[-1]
			img = request.get(image_url,5)
			f = open(name,'ab')
			f.write(img.content)
			f.close()
			print('保存完毕:%s' % (image_url))

	# 生成MD5
	def genearteMD5(self, str):
   		# 创建md5对象
		hl = hashlib.md5()
		# Tips
		# 此处必须声明encode
		# 否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
		hl.update(str.encode(encoding='utf-8'))

		# print('MD5加密前为 ：' + str)
		# print('MD5加密后为 ：' + hl.hexdigest())
		return hl.hexdigest()
	# print(self.img_urls)
	



amazon = Amazon()
# amazon.getdata('https://www.amazon.com/Bikini-Swimsuit-Family-Matching-Swimwear/dp/B07C6KQLK4/ref=pd_sim_193_2?_encoding=UTF8&pd_rd_i=B0798Q7CBW&pd_rd_r=03e5390e-7d11-11e8-8d25-e7cfe09295e4&pd_rd_w=UDsse&pd_rd_wg=aeLQW&pf_rd_i=desktop-dp-sims&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=7967298517161621930&pf_rd_r=6JJR419ZM6JR3BG31AGY&pf_rd_s=desktop-dp-sims&pf_rd_t=40701&refRID=6JJR419ZM6JR3BG31AGY&th=1')
		