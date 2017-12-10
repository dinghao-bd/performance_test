#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1
@author: ding hao
@mail: 619015618@qq.com
@file: adb.py
@time: 2017/12/9 17:35
"""
import os

# 请到GitHub上下载PyAdb安装，版本0.1.4
from pyadb import ADB


class AdbClient(object):
    def __init__(self):
        pass

    def visible(self):
        pass

    # 根据不同的平台获取环境变量中adb的path
    def get_path(self):
        if os.name == "nt":
            for line in os.environ.get("PATH").split(";"):
                if "platform-tools" in line:
                    return line
        elif os.name == "posix":
            for line in os.environ.get("PATH").split(":"):
                if "platform-tools" in line:
                    return line

    # 初始化PyAdb
    def get_adb_obj(self):
        adb_object = None

        adb_path = self.get_path()

        if os.name == "nt":
            adb_object = ADB(adb_path + "\\adb.exe")
        elif os.name == "posix":
            adb_object = ADB(str(adb_path) + "/adb")

        return adb_object


# 初始化AdbClient，方便外面直接调用
adb = AdbClient().get_adb_obj()
