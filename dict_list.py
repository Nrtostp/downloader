# coding: utf-8

import pickle
from os.path import exists
from config import msg_home
path=msg_home+'dict.data'

class dict_list:
	def __init__(self):
		if exists(path):
			with open(path,'rb') as f:
				self.__data=pickle.load(f)
		else:
			self.__data={}

	def add(self,url,obj):
		self.__data[url] = obj

	def get(self,url):
		return self.__data.get(url)
	
	def get_data(self):
		return self.__data

	def dump(self):
		with open(path,'wb') as f:
			pickle.dump(self.__data,f)

if __name__ == "__main__":
	dict_list=dict_list()
	print(dict_list.get_data())