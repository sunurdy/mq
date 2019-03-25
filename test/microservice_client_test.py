#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version:
@author:
@time: 2017/5/24 11:20
"""
import logging

from micro_service.mq import logger as mqlog
from micro_service.service_base import MicroService, logger

logging.basicConfig(format='%(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
logger.setLevel(logging.DEBUG)
mqlog.setLevel(logging.DEBUG)
# console = logging.StreamHandler()
# logger.addHandler(console)

AMQ_URI = "amqp://user:3^)NB@101.199.126.121:5672/api"

s = MicroService('s1', AMQ_URI, exchange='play')
print s.services.keys()
# queue = 'q1'
queue = s.service_task_queue('add')  # 's1.my'
callback_queue = s.client_callback_queue('add')  # 'q2'
print queue
print callback_queue





