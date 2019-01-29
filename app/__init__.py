# -*- coding:utf-8 -*-
import sys
from sanic import Sanic
import logging
from pythonjsonlogger import jsonlogger
''' 
@author: luochenxi
@time: 2019/1/29
@desc:

'''

app = Sanic(__name__)

logger = logging.getLogger('sanic')

logHandler = logging.StreamHandler(stream=sys.stdout)
fmt="%(asctime) %(levelname) %(filename) %(funcName) %(lineno) %(message)"
datefmt="%Y-%m-%dT%H:%M:%SZ%z"

formatter = jsonlogger.JsonFormatter(fmt=fmt, datefmt=datefmt,json_ensure_ascii=False)
logHandler.setFormatter(formatter)
logger.setLevel("INFO")
logger.addHandler(logHandler)

from app import views
