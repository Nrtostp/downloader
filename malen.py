#! /usr/bin/env python3
# coding : utf-8

from getopt import GetoptError, getopt
from sys import argv, exit
from download import D
from multiprocessing import Process
from upload import run
from time import sleep
from config import home,share_home
usage = """
用法： [-o <选项>] [<参数>]
-h					帮助信息
-v					版本号
-a	URL				添加一个下载链接
-al	Path				从文件中添加下载任务
-w					查看下载列表
-c					清空下载列表
-d	(临时下载目录)			开始下载任务
-f	FileName			查询共享库文件
-r					启动共享服务
-e					关闭共享服务
-q					退出程序
"""

version = """
版本 1.0 (Python-3.7.3)
Copyright 2019 Qianyri
please input '-h' for help
"""

def main():
	lists=[]
	p=-1
	while True:
		print('<<  ',end='')
		try:
			argv=input().split()
		except:
			continue
		if len(argv)==0:
			continue
		opt=argv[0]
		if opt=='-h':
			print(usage)
		elif opt=='-v':
			print(version)
		elif opt=='-a':
			try:
				url=argv[1]
				if url.find('http')==-1:
					print('The URL must begin with "http://" or "https://"')
				else :
					lists.append(url)
					print('done')
			except:
				print('please input url')
		elif opt=='-al':
			try:
				with open(argv[1],'r') as f:
					for url in f.readlines():
						url = url.strip('\n')
						if url.find('http') == -1:
							print('The url:'+url+' must begin with "http://" or "https://"')
						else:
							lists.append(url) 
				print('done')
			except:
				print('no such path')
		elif opt=='-w':
			for url in lists:
				print(url)
		elif opt=='-c':
			lists=[]
			print('task lists cleared')
		elif opt=='-d':
			if len(lists)==0:
				print('There is no task in the list')
			else:
				D.add(lists)
				lists=[]
				try:
					D.start(argv[1])
				except:
					D.start()
				D.stop()
		elif opt=='-f':
			try:
				D.search(argv[1])
			except:
				print('please input key word')
		elif opt=='-r':
			if p!=-1:
				print('server is running')
			else:
				print('share home is:'+share_home+' ,modify <config.json> to change')
				p=Process(target=run)
				p.start()
				D.insert()
				sleep(2)
		elif opt=='-e':
			if p!=-1:
				D.delete()
				p.terminate()
				p=-1
				print('server closed')
			else:
				print('no server running')
		elif opt=='-q':
			if p!=-1:
				D.delete()
				p.terminate()
				print('server closed')
			exit()
		else :
			print(usage)

if __name__ == "__main__":
	print(version)
	print('default download home:'+home)
	print('default share home:'+share_home)
	main()

