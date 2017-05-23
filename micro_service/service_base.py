#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2017/5/23 16:52
"""
from micro_service.mq import MQ


class MicroService(MQ):
    def __init__(self, amqp, exchange='play'):
        super(MicroService, self).__init__(amqp, exchange)
        self.services = {}

    def load_services(self):
        pass
