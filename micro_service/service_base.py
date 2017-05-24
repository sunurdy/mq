#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2017/5/23 16:52
"""
import logging
from uuid import uuid4

from gevent.monkey import patch_all

from micro_service.mq import MQ
from services.add import add_func
from services.sleep_func import sleep_function
patch_all()
logger = logging.getLogger(__name__)


class MicroService(MQ):
    def __init__(self, service_scope, amqp, exchange='play'):
        self.service_scope = service_scope
        super(MicroService, self).__init__(amqp, exchange)
        self.services = {}
        self.load_services()

    def load_services(self):
        # todo 加载所有标记的服务函数
        # 测试用 只加2个
        self.services.setdefault('add', add_func)
        self.services.setdefault('sleep', sleep_function)

    def service_queue(self, service):
        return "{0}.{1}".format(self.service_scope, service)

    def client_callback_queue(self, service):
        return "rpc_{0}.{1}".format(self.service_queue(service), uuid4())

    def start(self):
        def make_coroutine(service, func):
            def co():
                self.sub_task(self.service_queue(service=service), func)
            return co

        logger.info('------MICRO SERVICE START ------')
        for service, func in self.services.iteritems():
            print 5 * '-', '\n', 'service', service
            print 'queue:', self.service_queue(service=service)
            self.pool.spawn(make_coroutine(service, func),)
            # self.sub_task(self.service_queue(service=service), func)
        self.pool.join()

    #client
    def rpc(self, service):
        pass


            # region WORK TASK
            # endregion

            # region MANAGE TOOLS
            # endregion
