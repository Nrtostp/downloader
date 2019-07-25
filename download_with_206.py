# coding : utf-8

from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED
from threading import Lock
from config import range_size, chunk_size, max_threads, max_gevents, user_agents
from controler import controler
from os.path import exists
from queue import Queue
from random import randint
import requests
from traceback2 import format_exc
from logger import logger
from math import ceil
class downloader_with_206:
	def __init__(self):
		self.__excutor = ThreadPoolExecutor(max_threads)
		self.__tasks=[]

	def __get_agent(self):
		return user_agents[randint(0, len(user_agents)-1)]

	def __download(self,url,job,left,right,sess,file,lock):
		try:
			headers={}
			headers['Range']='bytes={}-{}'.format(left,right)
			headers['User-Agent']=self.__get_agent()
			for i in range(3):
				with sess.get(url,headers=headers,stream=True) as r:
					if r.status_code!=206:
						logger.warning(url+'-range:%d-%d try %d times' % (left, right,i))
						sleep(0.5)
						continue
					lock.acquire()
					file.seek(left)
					file.write(r.content)
					lock.release()
					controler.update(right-left+1)
					job['queue'].append((left,right))
				return
			logger.warning(url+'-range:%d-%d missing' % (left, right))
		except Exception as e:
			logger.error(format_exc())
		
	def __split(self,url,job):
		try:
			pool=Pool(max_gevents)
			lock=Lock()
			with open(job['path'], (exists(job['path']) and 'rb+') or 'wb') as file:
				with requests.Session() as sess:
					list_set=set(job['queue'])
					left,right=(-1,-1)
					while right<job['length']-1:
						left,right=(right+1,min(right+range_size,job['length']-1))
						if not (left,right) in list_set:
							pool.spawn(self.__download, url, job, left, right, sess, file,lock)
				pool.join()
			if len(job['queue'])<int(ceil(1.0*job['length']/range_size)):
				job['status']='miss'
				controler.miss()
				logger.debug(url+' miss')
			else:
				job['status']='done'
				controler.success()
				logger.debug(url+' done')
				print(url+' done')
			controler.dict_list.add(url, job)
		except Exception as e:
			logger.error(format_exc())

	def add(self,url,job):
		try:
			self.__tasks.append(self.__excutor.submit(self.__split,url,job))
		except Exception as e:
			logger.error(format_exc())


	def stop(self):
		try:
			wait(self.__tasks, return_when=ALL_COMPLETED)
		except Exception as e:
			logger.error(format_exc())


