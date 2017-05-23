#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2017/5/23 16:51
"""
from gevent import monkey
from gevent.pool import Pool
import contextlib
import logging
import uuid

import msgpack
import pika

monkey.patch_all()
logger = logging.getLogger(__name__)


class MQ(object):
    def __init__(self, amqp, exchange='center', pool_size=100):
        self.amqp = amqp
        self.exchange = exchange
        self.exchange_pub_sub = '%s_%s' % (exchange, 'pub_sub')
        self.pool = Pool(pool_size)

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

    def publish(self):
        """发布订阅"""
        pass

    def subscribe(self):
        pass

    def pub_task(self, queue, callback_queue, payload, correlation_id=None, ttl=None):
        """发布抢占任务,(client)"""

        def p(x): logger.warning(x)

        payload = self.encode_body(payload)
        with self.make_channel() as channel:
            channel.queue_declare(queue=callback_queue, exclusive=False)  # 发布者的队列
            channel.queue_declare(queue=queue, exclusive=False, auto_delete=False)  # 抢占的队列

            channel.basic_consume(p, no_ack=True, queue=callback_queue)
            flag = channel.basic_publish(exchange=self.exchange,
                                         routing_key=queue,
                                         body=payload,
                                         properties=pika.BasicProperties(
                                                 reply_to=callback_queue,
                                                 expiration="%d" % ttl if ttl else None,
                                                 message_id=str(uuid.uuid4()),
                                                 correlation_id=correlation_id)
                                         )
            logger.debug("flag %s" % flag)
            logger.debug("queue %s" % queue)
            logger.debug("callback_queue %s" % callback_queue)
            logger.debug("payload %s" % payload)

    def sub_task(self, queue, call_back_func):
        """服务端 消费者 抢占任务"""

        def on_request(ch, method, props, body):
            logger.debug('on_request')
            payload = self.decode_body(body)
            dargs, dkwargs = payload

            ch.basic_ack(delivery_tag=method.delivery_tag)
            # response = call_back_func(*dargs, **dkwargs)
            g = self.pool.spawn(call_back_func, *dargs, **dkwargs)
            g.join()
            logger.debug(g.value)

            res = self.encode_body(g.value)

            ch.basic_publish(exchange=self.exchange,
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(correlation_id=props.correlation_id),
                             body=self.encode_body(res))

        with self.make_channel() as channel:
            channel.queue_declare(queue=queue)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(on_request, queue=queue)
            logger.debug('about to consume')
            channel.start_consuming()

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
