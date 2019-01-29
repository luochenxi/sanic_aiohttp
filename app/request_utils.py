# -*- coding:utf-8 -*-
import ujson
from ast import literal_eval
''' 
@author: luochenxi
@time: 2018/11/9
@desc:

'''


async def post(session, url,parms):
    """
    第一版：request retrieval
    :param session:
    :param url:
    :param parms:
    :return:
    """
    try:
        async with session.post(url,json=parms,timeout=5) as response:
            data = await response.text()
            eval_data = literal_eval(data)
            dic_data = ujson.loads(eval_data)
            return {
                'ok': True,
                'headers': dict(response.headers),
                'status': response.status,
                'url': url,
                'data':dic_data
            }
    except Exception as e:
        return {
            'ok': False,
            'error': str(e),
            'url': url,
        }

async def post_v2(session, url,parms,semaphore):
    """
    第二版：新增信号量，限制并发。 request retrieval
    :param session:
    :param url:
    :param parms:
    :return:
    """
    try:
        async with semaphore:
            async with session.post(url,json=parms,timeout=5) as response:
                # dic_data = await response.json()
                data = await response.text()
                eval_data = literal_eval(data)
                dic_data = ujson.loads(eval_data)
                return {
                    'ok': True,
                    'headers': dict(response.headers),
                    'status': response.status,
                    'url': url,
                    'data':dic_data
                }
    except Exception as e:
        return {
            'ok': False,
            'error': str(e),
            'url': url,
        }


async def get(session, url,parms):
    try:
        async with session.get(url,params=parms) as response:
            data = await response.json()
            return {
                'ok': True,
                'headers': dict(response.headers),
                'status': response.status,
                'url': url,
                'data':data
            }
    except Exception as e:
        return {
            'ok': False,
            'error': str(e),
            'url': url,
        }

