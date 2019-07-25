# coding: utf-8
import os
import sys
from aiohttp import web
import json
import asyncio
import aiomysql
from logger import logger
from traceback2 import format_exc

DATABASES = {'host': '127.0.0.1', 'port': 3306,
			'user': 'root', 'password': 'Qianyri_123', 'db': 'mybatis'}


async def create_pool(loop, **kw):
	global mysql_pool
	try:
		mysql_pool = await aiomysql.create_pool(host=DATABASES['host'], port=DATABASES['port'], user=DATABASES['user'],
											password=DATABASES['password'], db=DATABASES['db'], loop=loop,
											charset=kw.get('charset', 'utf8'), autocommit=kw.get('autocommit', True),maxsize=kw.get('maxsize', 10), minsize=kw.get('minsize', 1))
	except:
		logger.error(format_exc())
	return mysql_pool


async def search(sql, args=(), size=None):
	try:
		async with mysql_pool.acquire() as conn:
			async with conn.cursor(aiomysql.DictCursor) as cur:
				await cur.execute(sql, args)
				if size:
					rs = await cur.fetchmany(size)
				else:
					rs = await cur.fetchall()
				return rs
	except:
		logger.error(format_exc())


async def execute(sql, args=()):
	try:
		async with mysql_pool.acquire() as conn:
			async with conn.cursor() as cur:
				try:
					await cur.execute(sql, args)
				except BaseException:
					await conn.rollback()
					return 0
				else:
					affected = cur.rowcount
					return affected
	except :
		logger.error(format_exc())


class view1(web.View):
	async def get(self):
		try:
			name = self.request.match_info.get('name')
			result = await search('select * from list where name like %s', ('%'+name+'%',))
			return web.json_response(data=result)
		except:
			logger.error(format_exc())


class view2(web.View):
	async def get(self):
		try:
			data = json.loads(await self.request.read())
			cnt=0;
			for x in data:
				cnt+= await execute('insert into list(name,path,length) value(%s,%s,%s)', (x['name'], x['path'],x['length'],))
			return web.json_response(data=cnt)
		except:
			logger.error(format_exc())


class view3(web.View):
	async def get(self):
		try:
			data = json.loads(await self.request.read())
			cnt=await execute('delete from list where path=%s', (data,))
			return web.json_response(data=cnt)
		except:
			logger.error(format_exc())


class view4(web.View):
	async def get(self):
		try:
			headers = {'content-type': 'text/html charset = utf-8'}
			return web.Response(status='200', headers=headers, body='hello world!')
		except:
			logger.error(format_exc())

def run():
	try:
		loop = asyncio.get_event_loop()
		loop.run_until_complete(create_pool(loop))
		app = web.Application()
		app.router.add_route('*', '/search/{name}', view1)
		app.router.add_route('*', '/insert', view2)
		app.router.add_route('*', '/del', view3)
		app.router.add_route('*', '/', view4)
		web.run_app(app, host='0.0.0.0', port=9000)
	finally:
		loop.close()

if __name__ == "__main__":
	try:
		pid = os.fork()
		if pid > 0 :
			sys.exit(0)
	except OSError as e:
		sys.exit(1)
	os.chdir("/")
	os.setsid()
	os.umask(0)
	try:
		pid = os.fork()
		if pid > 0:
			print ("Daemon PID %d" % pid)
			sys.exit(0)
	except OSError as  e:
		sys.exit(1)
	run()
