#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2017/5/23 16:52
"""
from micro_service.service_base import MicroService


class MicroServiceClient(MicroService):
    def __init__(self, service_scope, amqp, exchange):
        super(MicroServiceClient, self).__init__(service_scope, amqp, exchange=exchange)
