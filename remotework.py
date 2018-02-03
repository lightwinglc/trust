#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ConfigParser
import pexpect
from pexpect import pxssh
import argparse
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 配置文件类，从配置文件中获取主机列表，初始化输入参数为配置文件路径
class WorkConf(object):
    def __init__(self, file):
        self.file = file
        self.parse_conf()

    def parse_conf(self):
        config = ConfigParser.ConfigParser()
        with open(self.file, 'r') as cfgfile:
            config.readfp(cfgfile)
            self.hostsmap = config.get('hosts', 'hostsmap')
            self.username = config.get('hosts', 'username')
            self.password = config.get('hosts', 'password')
            self.scpsourcedir = config.get('work', 'scpsourcedir')
            self.scptargetdir = config.get('work', 'scptargetdir')
            self.worklist = config.get('work', 'worklist')


# 完成远程工作的类，初始化传入配置类
class RemoteWork(object):
    def __init__(self, config):
        self.hostsmap = eval(config.hostsmap)
        self.username = config.username
        self.password = config.password
        self.scpsourcedir = config.scpsourcedir
        self.scptargetdir = config.scptargetdir
        self.worklist = eval(config.worklist)

    def do_allwork(self):
        # 遍历主机，依次完成工作
        for host in self.hostsmap.keys():
            self.do_singlework(host)

    # 在单台主机上执行工作
    def do_singlework(self, host):
        ssh_client = pxssh.pxssh()
        ssh_client.login(host, self.username, self.password)

        # 建目标目录
        father_path = os.path.abspath(os.path.dirname(self.scptargetdir) + os.path.sep + ".")
        ssh_client.sendline('mkdir -p %s'%father_path)
        ssh_client.prompt()
        print(ssh_client.before)

        # 复制包到目标机器
        (command_output, exitstatus) = pexpect.run('scp -r %s %s@%s:%s'
            %(self.scpsourcedir, self.username, host, self.scptargetdir), withexitstatus=1)
        print command_output
        if exitstatus != 0:
            return

        # 执行命令
        for workcmd in self.worklist:
            ssh_client.sendline(workcmd)
            ssh_client.prompt()
            print(ssh_client.before)

        ssh_client.logout()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="path of config file")
    args = parser.parse_args()

    myconf = WorkConf(args.config)
    mywork = RemoteWork(myconf)
    mywork.do_singlework("132.252.130.15")


if __name__ == '__main__':
    main()