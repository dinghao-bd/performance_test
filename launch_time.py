#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1
@author: ding hao
@mail: 619015618@qq.com
@file: launch_time.py
@time: 2017/11/22 10:43
"""
import csv
import os

import time


class APP(object):
    def __init__(self, package_name, activity_name, is_cold_launch):
        self.package_name = package_name
        self.activity_name = activity_name
        self.is_cold_launch = is_cold_launch
        self.result = None

    # 启动app
    def start_app(self):
        cmd = "adb shell am start -W -n %s" % (self.package_name + "/" + self.activity_name)
        self.result = os.popen(cmd)

    # 关闭app
    def stop_app(self):
        if self.is_cold_launch:
            cmd = "adb shell am force-stop %s" % (self.package_name)
        else:
            cmd = "adb shell input keyevent 3"
        os.popen(cmd)

    # 获取启动时间
    def get_launch_time(self):
        for line in self.result.readlines():
            if "ThisTime" in line:
                return line.split(":")[1]

    # 获取测试前的时间
    def get_launch_before_time(self):
        return time.time()

    # 获取测试结束的时间
    def get_launch_after_time(self):
        return time.time()


class Controller(object):
    def __init__(self, count, package_name, activity_name, is_cold_launch=True):
        self.app = APP(package_name, activity_name, is_cold_launch)
        self.launch_time = [("test time", "launch time")]
        self.counter = count

    # 运行测试
    def run(self):
        for i in xrange(0, self.counter):
            self.app.start_app()
            time.sleep(5)
            self.app.stop_app()
            self.launch_time.append(
                (time.strftime("%Y-%m-%d %H:%M:%S"), self.app.get_launch_time()[:-1]))

    # 保存测试结果到CSV文件
    def save_result_to_csv(self):
        csvfile = file("launchtime.csv", "wb")
        write = csv.writer(csvfile)
        write.writerows(self.launch_time)
        csvfile.close()


if __name__ == "__main__":
    control = Controller(5, "com.chaozh.iReaderFree", "com.chaozh.iReader.ui.activity.WelcomeActivity")
    control.run()
    control.save_result_to_csv()
