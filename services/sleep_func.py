#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2017/5/24 10:24
"""
import datetime
import time


def sleep_function(m, n):
    print 'start@', datetime.datetime.now()
    time.sleep(5)
    print 'end@', datetime.datetime.now()
    return str(datetime.datetime.now())
