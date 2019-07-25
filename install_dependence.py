# coding :utf-8
from os import system
import platform
try:
	import requests
except:
	system('pip3 install requests')
try:
	import progressbar
except:
	system('pip3 install progressbar')
try:
	import gevent
except:
	system('pip3 install gevent')
try:
	import logging
except:
	system('pip3 install logging')
try:
	import traceback2
except:
	system('pip3 install traceback2')
try:
	import aiohttp
except:
	system('pip3 install aiohttp')
try:
	import asyncio
except:
	system('pip3 install asyncio')
try:
	import aiomysql
except:
	system('pip3 install aiomysql')
try:
	import cryptography
except:
	system('pip3 install cryptography')
try:
	import aiohttp_session
except:
	system('pip3 install aiohttp_session')
try:
	import coloredlogs
except:
	system('pip3 install coloredlogs')

if __name__ == "__main__":	
	print('Please open file <config.json> change default setting!')
	if platform.system()=='Linux':
		print('Open it ?y/n')
		s=input()
		if s=='y':
			system('vi config.json')







