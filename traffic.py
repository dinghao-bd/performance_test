#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1
@author: ding hao
@mail: 619015618@qq.com
@file: traffic.py
@time: 2017/12/9 17:30
"""
import csv
import os
import string
import time


# 控制类
class Controller(object):
    def __init__(self, package_name, count):
        self.traffic = [("test time", "traffic")]
        self.counter = count
        self.package_name = package_name

    # 单次测试
    def test_process(self):
        cmd = None
        if os.name == "nt":
            cmd = "adb shell ps | findstr %s" % self.package_name
        elif os.name == "posix":
            cmd = "adb shell ps | grep %s" % self.package_name

        result = os.popen(cmd)

        pid = result.readlines()[0].split(" ")[5]

        traffic = os.popen("adb shell cat /proc/" + pid + "/net/dev")
        receive1 = receive2 = transmit1 = transmit2 = None
        for line in traffic:
            if "eth0" in line:
                line = "#".join(line.split())
                receive1 = line.split("#")[1]
                transmit1 = line.split("#")[9]
            elif "eth1" in line:
                line = "#".join(line.split())
                receive2 = line.split("#")[1]
                transmit2 = line.split("#")[9]

        alltraffic = string.atoi(receive1) + string.atoi(transmit1) + string.atoi(receive2) + string.atoi(transmit2)
        alltraffic = alltraffic / 1024

        curren_time = self.get_test_time()

        self.traffic.append((curren_time, alltraffic))

    # 多次测试
    def run(self):
        for i in xrange(self.counter):
            self.test_process()
            # 间隔60s取一次流量值
            time.sleep(60)

    # 获取执行时间
    def get_test_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")

    # 保存数据
    def save_result_to_csv(self):
        csv_file = file("traffic.csv", "wb")
        write = csv.writer(csv_file)
        write.writerows(self.traffic)
        csv_file.close()


if __name__ == "__main__":
    Controller = Controller("com.tencent.mm", 5)
    Controller.run()
    Controller.save_result_to_csv()
