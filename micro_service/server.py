#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2017/5/23 16:52
"""
from micro_service.service_base import MicroService


class MicroService_Server(MicroService):
    def __init__(self, amqp, exchange):
        super(MicroService_Server, self).__init__(amqp, exchange=exchange)

    def run(self):
        pass

    def listen_task(self):
        pass

    def listen_manage(self):
        pass

