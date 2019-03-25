#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2017/5/23 16:52
"""
from micro_service.service_base import MicroService


class MicroServiceServer(MicroService):
    def __init__(self, service_scope, amqp, exchange):
        super(MicroServiceServer, self).__init__(service_scope, amqp, exchange=exchange)

    def run(self):
        pass

    def listen_task(self):
        pass

    def listen_manage(self):
        pass
