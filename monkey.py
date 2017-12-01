#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1
@author: ding hao
@mail: 619015618@qq.com
@file: monkey.py
@time: 2017/12/1 17:30
"""

import os


class Monkey(object):
    def __init__(self, device_id):
        self.device_id = device_id

    def exc(self):
        cmd = 'adb -s %s shell "monkey -s 1000 --throttle 1000 -p com.zhangyue.iReader.Eink --pct-syskeys 0 --pct-anyevent 0 --pct-majornav 0 --ignore-timeouts --ignore-security-exceptions --ignore-crashes -v -v -v 100000000 > /mnt/sdcard/log.txt 2>&1 &"' % self.device_id
        result = os.popen(cmd).read()
        return result


class Controller(object):
    def __init__(self, device_id):
        self.monkey = Monkey(device_id)

    def test_monkey(self):
        self.monkey.exc()

    def run(self):
        self.test_monkey()
