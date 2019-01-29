# -*- coding:utf-8 -*-
# local imports
from app import app
from sanic_mongo import Mongo
from sanic import response
import aiohttp
import asyncio
from aiohttp import TCPConnector
import uvloop
''' 
@author: luochenxi
@time: 2018/11/8
@desc:

'''
# initialize imports
# mongo_uri = "mongodb://{host}:{port}/{database}".format(
#     database='test',
#     port=3006,
#     host='test.com'
# )
# Mongo.SetConfig(app,deepnet_hash=mongo_uri)
# Mongo(app)


class ReuseableTCPConnector(TCPConnector):
    """
    多路复用TCP连接池
    """
    def __init__(self, *args, **kwargs):
        super(ReuseableTCPConnector, self).__init__(*args, **kwargs)
        self.old_proto = None

    async def connect(self, req, *args, **kwargs):
        new_conn = await super(ReuseableTCPConnector, self)\
                                .connect(req, *args, **kwargs)

        self.old_proto = new_conn._protocol
        return new_conn


class ChattyPolicy(uvloop.EventLoopPolicy):
    def get_event_loop(self):
        loop = super().get_event_loop()
        print('getting event loop {}'.format(id(loop)))
        return loop

    def set_event_loop(self, loop):
        super().set_event_loop(loop)
        print('setting event loop {}'.format(id(loop)))

    def new_event_loop(self):
        loop = super().new_event_loop()
        print('new event loop {}'.format(id(loop)))
        return loop


@app.listener('before_server_start')
async def before_server_start(app, loop):
    print('before_server_start.')
    # connector = aiohttp.TCPConnector(limit=100, limit_per_host=100) # 限制并发数

    asyncio.set_event_loop(loop)
    app.policy_asyncio =asyncio

    connector = ReuseableTCPConnector(
                   verify_ssl=False,
                   loop=loop,
                   # keepalive_timeout=600,
                   limit=0
               )
    app.semaphore = asyncio.Semaphore(400)
    app.client_session = await aiohttp.ClientSession(connector=connector,loop=loop).__aenter__()

@app.listener('after_server_start')
async def notify_server_started(app, loop):
    print('Server successfully started.')


@app.listener('before_server_stop')
async def notify_server_stopping(app, loop):
    print('Server shutting down...')


@app.listener('after_server_stop')
async def after_server_stop(app, loop):
    print('Server successfully shutdown.')
    await app.client_session.__aexit__(None, None, None)


from app.infter_v2 import xiuxiu_v2

def index(request):
    return response.text("Hello ApiServer")

# Routes
app.add_route(index, '/')
app.add_route(xiuxiu_v2, 'hash/v2')

