# coding: utf-8
from aiohttp import web
import asyncio
from os.path import exists,getsize
from config import share_home, port
import time
import base64
from cryptography import fernet
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from traceback2 import format_exc
from logger import logger

class view(web.View):
	async def get(self):
		try:
			session = await get_session(self.request)
			name = self.request.match_info.get('name')
			if not self.request.headers.get('Range'):
				headers = {'content-type': 'text/html charset = utf-8'}
				return web.Response(status='200', headers=headers, body='hello world!')
			ll, rr = self.request.headers['Range'].replace('bytes=', '').split('-')
			left=int(ll)
			right=int(rr)
			path = share_home+name
			if not exists(path):
				return web.Response(status='404')
			else:
				headers={}
				headers['Content-Range']='bytes '+ll+'-'+rr+'/'+str(getsize(path))
				with open(path, 'rb') as f:
					f.seek(left)
					body= f.read(right-left+1)
				return web.Response(status='206',headers=headers,body=body)
		except:
			logger.error(format_exc())

def run():
	app = web.Application()
	fernet_key = fernet.Fernet.generate_key()
	secret_key = base64.urlsafe_b64decode(fernet_key)
	setup(app, EncryptedCookieStorage(secret_key))
	app.router.add_route('*', '/{name}', view)
	web.run_app(app, host='0.0.0.0', port=port)

