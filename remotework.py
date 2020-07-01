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
    def __init__(self, config_file):
        self.config_file = config_file
        config = ConfigParser.ConfigParser()
        with open(self.config_file, 'r') as config_file:
            config.readfp(config_file)
            self.hosts_map = config.get('hosts', 'hosts_map')
            self.username = config.get('hosts', 'username')
            self.password = config.get('hosts', 'password')
            self.scp_map = config.get('work', 'scp_map')
            self.work_list = config.get('work', 'work_list')


# 完成远程工作的类，初始化传入配置类
class RemoteWork(object):
    def __init__(self, config):
        self.hosts_map = eval(config.hosts_map)
        self.username = config.username
        self.password = config.password
        self.scp_map = eval(config.scp_map)
        self.work_list = eval(config.work_list)

    def do_all_work(self):
        # 遍历主机，依次完成工作
        for host in self.hosts_map.keys():
            self.do_single_work(host)

    # 在单台主机上执行工作
    def do_single_work(self, host):
        print 'begin host %s work:#######################################################' % host
        # 登录
        ssh_client = pxssh.pxssh()
        ssh_client.login(host, self.username, self.password)

        # 删除目标目录
        # ssh_client.sendline('rm -rf %s' % self.scptargetdir)
        # ssh_client.prompt()
        # print(ssh_client.before)

        # 建目标目录
        # father_path = os.path.abspath(os.path.dirname(self.scptargetdir) + os.path.sep + ".")
        # ssh_client.sendline('mkdir -p %s'%father_path)
        # ssh_client.prompt()
        # print(ssh_client.before)

        # 复制包到目标机器
        # (command_output, exitstatus) = pexpect.run('scp -r %s %s@%s:%s'
        #     %(self.scpsourcedir, self.username, host, self.scptargetdir), withexitstatus=1)

        # 复制文件到目标位置
        for sourcefile in self.scp_map.keys():
            # 检查目标目录是否存在，不存在则新建
            father_path = os.path.abspath(os.path.dirname(self.scp_map[sourcefile]))
            if father_path != os.path.abspath('/'):
                ssh_client.sendline('mkdir -p %s' % father_path)
                ssh_client.prompt()
                print(ssh_client.before)

            # 进行scp操作
            (command_output, exit_status) = pexpect.run('scp %s %s@%s:%s'
                                                        % (sourcefile, self.username, host, self.scp_map[sourcefile]),
                                                        withexitstatus=1)
            print command_output
            if exit_status != 0:
                return

        # 执行命令
        for work_cmd in self.work_list:
            ssh_client.sendline(work_cmd)
            ssh_client.prompt()
            print(ssh_client.before)

        ssh_client.logout()
        print 'end host %s work:#######################################################' % host


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="path of config file")
    args = parser.parse_args()

    config_object = WorkConf(args.config)
    work_object = RemoteWork(config_object)
    work_object.do_all_work()
    # mywork.do_singlework("132.252.130.11")


if __name__ == '__main__':
    main()
