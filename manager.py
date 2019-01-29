# -*- coding: utf-8 -*-

import uvloop
import asyncio
from app import app

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002,loop=loop,workers=6,debug=False, access_log=False)