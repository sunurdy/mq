#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2017/5/23 19:23
"""
from gevent import monkey

monkey.patch_all()
import logging
from micro_service.mq import MQ, logger
logging.basicConfig(format='%(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
logger.setLevel(logging.DEBUG)
# console = logging.StreamHandler()
# logger.addHandler(console)

AMQ_URI = "amqp://user:3^)NB@101.199.126.121:5672/api"

mq = MQ(AMQ_URI, exchange='play')
queue = 's1.sleep'
# queue = 'q1'
callback_queue = 'q2'


def func(n, m):
    import datetime, time
    print 'start', datetime.datetime.now()
    time.sleep(5)
    print 'end', datetime.datetime.now()
    return n + 1 + m


#
print mq.subscribe_queue(callback_queue)
import nameko