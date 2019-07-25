# codig : utf-8

from threading import Lock
from progressbar import ProgressBar, Timer, FileTransferSpeed, UnknownLength
from dict_list import dict_list
class control:
	def __init__(self):
		self.__locks = {i: Lock() for i in ('s', 'f', 'm', 'length')}
		self.__pbar = ProgressBar(
			widgets=[Timer(), ' ', FileTransferSpeed()], maxval=UnknownLength)
	
	def init(self, works=0):
		self.__works = works
		self.__s = 0
		self.__f = 0
		self.__m = 0
		self.__a = 0
		self.__length = 0
		self.dict_list=dict_list()
		self.__pbar.start()

	def success(self):
		if self.__locks['s'].acquire():
			self.__s+=1
			self.__locks['s'].release()
	
	def fail(self):
		if self.__locks['f'].acquire():
			self.__f+=1
			self.__locks['f'].release()
	
	def miss(self):
		if self.__locks['m'].acquire():
			self.__m+=1
			self.__locks['m'].release()
	
	def update(self,length):
		if self.__locks['length'].acquire():
			self.__length+=length
			self.__pbar.update(self.__length)
			self.__locks['length'].release()
		
	def done(self):
		self.__a += 1
	
	def stop(self):
		self.__pbar.finish()
		self.dict_list.dump()
		print('total:%d  success:%d  fail:%d  miss:%d  already_done:%d' %
		      (self.__works, self.__s, self.__f, self.__m, self.__a))

controler=control()

