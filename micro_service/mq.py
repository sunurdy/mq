#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2017/5/23 16:51
"""
import contextlib
import logging
import os
import uuid

import msgpack
import pika
from gevent.monkey import patch_all
from gevent.pool import Pool

patch_all()
logger = logging.getLogger(__name__)


class MQ(object):
    def __init__(self, amqp, exchange='center', gevent_pool_size=100):
        self.amqp = amqp
        self.exchange = exchange
        self.exchange_pub_sub = '%s_%s' % (exchange, 'pub_sub')
        self.pool = Pool(gevent_pool_size)

        connection = pika.BlockingConnection(pika.URLParameters(amqp))
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange, exchange_type='topic')
        channel.exchange_declare(exchange=self.exchange_pub_sub, exchange_type='fanout')
        connection.close()

    @contextlib.contextmanager
    def make_channel(self):
        connection = pika.BlockingConnection(pika.URLParameters(self.amqp))
        try:
            channel = connection.channel()
            yield channel
        finally:
            connection.close()

    def pub_task(self, queue, callback_queue, payload, correlation_id=None, ttl=None):
        """发布抢占任务,(client)"""

        encode_payload = self.encode_body(payload)
        with self.make_channel() as channel:
            channel.queue_declare(queue=callback_queue, exclusive=False, auto_delete=True)  # 发布者的队列
            channel.queue_declare(queue=queue, exclusive=False)  # 抢占的队列

            flag = channel.basic_publish(exchange=self.exchange,
                                         routing_key=queue,
                                         body=encode_payload,
                                         properties=pika.BasicProperties(
                                                 reply_to=callback_queue,
                                                 expiration="%d" % ttl if ttl else None,
                                                 message_id=str(uuid.uuid4()),
                                                 correlation_id=correlation_id)
                                         )

            logger.debug("pub_task =====================")
            logger.debug("flag %s" % flag)
            logger.debug("queue %s" % queue)
            logger.debug("callback_queue %s" % callback_queue)
            logger.debug(payload)
            logger.debug("pub_task =====================END")

    def sub_task(self, queue, call_back_func):
        """服务端 消费者 抢占任务 并交给回调函数"""

        def on_request(ch, method, props, body):
            def run(*dargs, **dkwargs):
                res = call_back_func(*dargs, **dkwargs)
                logger.debug('---run function of: {0}  @pid: {1}'.format(call_back_func.__name__, os.getpid()))
                logger.debug('---*dargs: {0}, **dkwargs: {1}'.format(dargs, dkwargs))
                logger.debug('---greenlet result: {0}'.format(res))
                res = self.encode_body(res)
                ch.basic_publish(exchange=self.exchange,
                                 routing_key=props.reply_to,
                                 properties=pika.BasicProperties(correlation_id=props.correlation_id),
                                 body=self.encode_body(res))

            payload = self.decode_body(body)
            dargs, dkwargs = payload
            ch.basic_ack(delivery_tag=method.delivery_tag)
            # response = call_back_func(*dargs, **dkwargs)
            self.pool.spawn(run, *dargs, **dkwargs)

        with self.make_channel() as channel:
            channel.queue_declare(queue=queue)
            channel.queue_bind(queue=queue, exchange=self.exchange, routing_key=queue)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(on_request, queue=queue)
            logger.debug(queue)
            logger.debug('about to consume')
            channel.start_consuming()

    def subcribe_queue(self, callback_queue):
        """客户端 监听消息并返回，"""
        with self.make_channel() as channel:
            channel.queue_declare(queue=callback_queue, auto_delete=True)
            channel.basic_qos(prefetch_count=1)
            # channel.basic_consume(on_request, queue=queue)
            logger.debug('about to listen queue')
            # channel.start_consuming()

    def publish(self):
        """发布订阅"""
        pass

    def subscribe(self):
        pass

    def encode_body(self, message):
        rdata = msgpack.dumps(message)
        return rdata

    def decode_body(self, message):
        rdata = msgpack.loads(message)
        return rdata

        # def create_queue(self, queue, exclusive=False, **kwargs):
        #     with self.make_channel() as channel:
        #         return channel.queue_declare(queue=queue, exclusive=exclusive, **kwargs)
        #
        # def queue_join_exchange(self, queue, exchange, routing_key, **kwargs):
        #     """Bind the queue to the specified exchange (topic mode)"""
        #     with self.make_channel() as channel:
        #         channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key, **kwargs)
