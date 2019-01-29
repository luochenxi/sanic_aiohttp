# -*- coding:utf-8 -*-
import os
from sanic import response
from app.request_utils import get,post
from app import logger as Log
from app import app

''' 
@author: luochenxi
@time: 2018/11/8
@desc:

'''

pools_strs = os.environ.get('HASH_ALL_DATA_RETRIEVE_DOMAIN','')
search_mult_urls=["http://{}:5505/search_mult_features".format(p_host) for p_host in pools_strs.split(",")]


async def xiuxiu_v2(request):
    params =request.args.get("image")

    post_infos = await app.policy_asyncio.gather(
        *[post(app.client_session, search_mult_url, params) for search_mult_url in search_mult_urls])

    return response.json(post_infos,headers={'Access-Control-Allow-Origin': '*'})


