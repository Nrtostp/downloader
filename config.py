# coding : utf-8
from json import loads,dumps

with open('config.json','r') as f:
    configs=loads(f.read())

range_size=configs['MB']
chunk_size=configs['KB']
max_works=configs['max-works']
max_threads=configs['max-threads']
max_gevents=configs['max-gevents']
user_agents=configs['user-agents']
home=configs['home']
share_home=configs['home']
msg_home=configs['msg-home']
port=configs['port']
server_bind=configs['server-bind']

