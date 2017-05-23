#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2017/5/23 16:52
"""
from micro_service.service_base import MicroService


class MicroService_Client(MicroService):
    def __init__(self, amqp, exchange):
        super(MicroService_Client, self).__init__(amqp, exchange=exchange)

