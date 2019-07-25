# coding : utf-8

from config import user_agents,max_works,home,share_home,server_bind,port
from download_with_206 import downloader_with_206
from download_without_206 import downloader_whithout_206
from controler import controler
from logger import logger
from queue import Queue
from random import randint
from os.path import basename,exists,getsize
from os import walk
from urllib import parse
import requests
from traceback2 import format_exc
from time import time
import json
import re


class downloader:
	def __init__(self):
		try:
			self.__downloader_with_206=downloader_with_206()
			self.__downloader_without_206=downloader_whithout_206()
			self.__queue=Queue(max_works)
			self.host=''
		except Exception as e:
			logger.error(format_exc())

	def __get_filename(self, url):
		name = basename(parse.unquote(
			url.split('/')[-1])) or str(int(round(time() * 1000)))+'.html'
		if len(name)>50:
			return name[-50:]
		else:
			return name

	def __get_agent(self):
		return user_agents[randint(0, len(user_agents)-1)]
	
	def search(self,name):
		lists=[]
		types=['B','KB','MB','GB']
		with requests.get('http://'+server_bind+'/search/'+name, stream=True) as r:
			lists = json.loads(r.content)
		print('get %d files' %(len(lists),))
		if len(lists)>0:
			print('%-50s%-80s%-23s' % ('文件名','文件URL','文件大小',))
			for x in lists:
				type_id=0;
				length=1.0*int(x['length'])
				while length/1024>1 and type_id<4:
					type_id+=1
					length/=1024
				print('%-50s%-80s%18.2f%-2s' % (x['name'],'http://'+x['path']+'/'+x['name'], length,types[type_id],))

	def insert(self):
		with requests.get('http://'+server_bind, stream=True) as r:
			self.host = r.raw._connection.sock.getsockname()[0]
		list_ = []
		for root, dirs, files in walk(share_home):
			for x in files:
				one = {}
				one['name'] = x
				one['path'] = self.host+':'+port
				one['length'] = getsize(share_home+x)
				list_.append(one)
			break
		data = json.dumps(list_)
		headers = {"content-type": "application/json"}
		with requests.get('http://'+server_bind+'/insert', headers=headers, data=data, stream=True) as r:
			logger.debug('upload %d files' % (json.loads(r.content),))

	def delete(self,path=None):
		if path==None:
			if self.host=='':
				return
			path=self.host+':'+port
			self.host=''
		data = json.dumps(path)
		headers = {"content-type": "application/json"}
		with requests.get('http://'+server_bind+'/del', headers=headers, data=data, stream=True) as r:
			logger.debug('unupload %d files' % (json.loads(r.content),))

	def __allocation(self,url,home_i):
		while True:
			try:
				with requests.get(url) as r:
					if r.status_code>300 and r.status_code<400:
						url=r.headers['Location']
					else:
						break
			except:
				logger.error('invaliable url: '+url)
				path=url.split('/')[2]
				if re.search('[0-9]+\.[0-9]+\.+[0-9]+\.[0-9]+\:[0-9]+', path):
					self.delete(path)
				controler.fail()
				return
		job=controler.dict_list.get(url)
		if job==None or not exists(job['path']):
			headers={'Range':'bytes=0-0'}
			headers['User-Agent']=self.__get_agent()
			try:
				with requests.get(url,headers=headers) as r:
					job={}
					job['status']='doing'
					job['path']=home_i+self.__get_filename(url)
					if r.status_code == 206:
						job['code']=206
						job['length']=int(r.headers['Content-Range'].split('/')[-1])
						job['queue']=[]
						self.__downloader_with_206.add(url,job)
					elif r.status_code == 200:
						job['code']=200
						self.__downloader_without_206.add(url,job)
					else:
						controler.fail()
						logger.warning(url+'   status-code:%d'%r.status_code)
			except Exception as e:
				logger.error(format_exc())
				controler.fail()
				print('invaliable url:'+url)
		else:
			if job['status'] == 'done' and exists(job['path']):
				controler.done()
				logger.debug(url+' already done')
			elif job['code']==206:
				self.__downloader_with_206.add(url,job)
			else:
				self.__downloader_without_206.add(url,job)

	def add(self,urls):
		try:
			for url in urls:
				self.__queue.put(url)
		except Exception as e:
			logger.error(format_exc())

	def start(self,home_i=home):
		try:
			controler.init(self.__queue.qsize())
			while not self.__queue.empty():
				self.__allocation(self.__queue.get(),home_i)
		except Exception as e:
			logger.error(format_exc())

	def stop(self):
		try:
			self.__downloader_with_206.stop()
			self.__downloader_without_206.stop()
			controler.stop()
		except Exception as e:
			logger.error(format_exc())

D=downloader()
