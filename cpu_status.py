#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1
@author: ding hao
@mail: 619015618@qq.com
@file: launch_time.py
@time: 2017/11/26 17:43
"""
import csv
import os

import time


class Controller(object):
    def __init__(self, package_name, count=1):
        self.cpu_status = [("test time", "cpu status")]
        self.counter = count
        self.package_name = package_name

    # 运行入口，10秒运行一次
    def run(self):
        for i in xrange(0, self.counter):
            self.test_process()
            time.sleep(10)

    # 测试方法，Windows平台下，使用findstr，Mac和Linux平台下，使用grep
    def test_process(self):
        cmd = "adb shell dumpsys cpuinfo | findstr %s" % self.package_name
        test_time = self.get_test_time()
        result = os.popen(cmd).readlines()
        for result_them in result:
            self.cpu_status.append((test_time, result_them.split("%")[0].lstrip()))

    # 获取执行时间
    def get_test_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")

    # 保存测试结果到csv文件
    def save_result_to_csv(self):
        csv_file = file("cpu_status.csv", "wb")
        write = csv.writer(csv_file)
        write.writerows(self.cpu_status)
        csv_file.close()


if __name__ == "__main__":
    Controller = Controller("com.tencent.mm", 5)
    Controller.test_process()
    Controller.save_result_to_csv()
