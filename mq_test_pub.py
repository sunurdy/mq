#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2017/5/23 19:23
"""
import logging


from micro_service.mq import MQ, logger
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
logger.addHandler(console)

AMQ_URI = "amqp://user:3^)NB@101.199.126.121:5672/api"

mq = MQ(AMQ_URI)
queue = 'q1'
# queue = 's1.my'
callback_queue = 'q2'


def func():
    return 1 + 1



mq.pub_task(queue, callback_queue, payload=([1], {}))
