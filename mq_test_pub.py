#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2017/5/23 19:23
"""
import logging

from micro_service.mq import MQ, logger
logging.basicConfig(format='%(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
logger.setLevel(logging.DEBUG)
# console = logging.StreamHandler()
# logger.addHandler(console)

AMQ_URI = "amqp://user:3^)NB@101.199.126.121:5672/api"

mq = MQ(AMQ_URI, exchange='play')
# queue = 'q1'
# queue = 's1.my'
queue = 's1.sleep'
callback_queue = 'q2'

mq.pub_task(queue, callback_queue, payload=([1, 2], {}))
