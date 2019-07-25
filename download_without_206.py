# coding : utf-8

from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
from config import chunk_size,max_gevents,user_agents
from controler import controler
from random import randint
import requests
from traceback2 import format_exc
from logger import logger

class downloader_whithout_206:
	def __init__(self):
		self.__pool=Pool(max_gevents)

	def __get_agent(self):
		return user_agents[randint(0,len(user_agents)-1)]

	def __download(self,url,job):
		try:
			headers={'User-Agent':self.__get_agent()}
			with requests.get(url,headers=headers,stream=True) as r:
				if r.status_code!=200:
					logger.warning(url+'status_code:%d'% r.status_code)
					job['status']='fail'
					controler.dict_list.add(url,job)
					controler.fail()
					logger.error(url+' fail')
					return
				with open(job['path'], 'wb') as f:
					for con in r.iter_content(chunk_size=chunk_size):
						f.write(con)
						controler.update(len(con))
			job['status']='done'
			controler.dict_list.add(url,job)
			controler.success()
			print(url+' done')
			logger.debug(url+' done')
		except Exception as e:
			logger.error(format_exc())

	def add(self,url,job):
		try:
			self.__pool.spawn(self.__download,url,job)
		except Exception as e:
			logger.error(format_exc())
	
	def stop(self):
		try:
			self.__pool.join()
		except Exception as e:
			logger.error(format_exc())

	

