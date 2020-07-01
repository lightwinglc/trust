#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ConfigParser
import sys

import pexpect
import argparse


# 配置文件类，从配置文件中获取主机列表、用户名和密码，初始化输入参数为配置文件路径
class TrustConf(object):
    def __init__(self, config_file):
        if config_file is None:
            print 'must set path of config file'
            sys.exit()
        self.config_file = config_file
        config = ConfigParser.ConfigParser()
        with open(self.config_file, 'r') as config_io:
            config.readfp(config_io)
            self.hosts_map = config.get('hosts', 'hosts_map')
            self.username = config.get('hosts', 'username')
            self.password = config.get('hosts', 'password')


# 在指定的主机上生成ssh秘钥，参数为主机IP，用户名和密码，已有key文件不进行覆盖
def remote_gen_key(host, username, password):
    command = 'ssh-keygen -t rsa'
    ssh_new_key = 'Are you sure you want to continue connecting'
    ssh_key_file = 'Enter file in which to save the key'
    ssh_passphrase = 'Enter passphrase'
    ssh_re_put_passphrase = 'Enter same passphrase again'
    ssh_over_write = 'Overwrite'
    ssh_password_error = 'Permission denied, please try again.'
    child = pexpect.spawn('ssh -l %s %s %s' % (username, host, command))
    while True:
        i = child.expect([pexpect.EOF, pexpect.TIMEOUT, ssh_new_key, 'password: ', ssh_key_file, ssh_passphrase,
                          ssh_re_put_passphrase, ssh_over_write, ssh_password_error])
        # 执行完退出
        if i == 0:
            print 'Host %s generating public/private rsa key pair OK.' % host
            break
        # 登录超时
        if i == 1:
            print 'ssh time out, error info:'
            print child.before, child.after
            break
        # 接收ssh新的key
        if i == 2:
            child.sendline('yes')
        # 输入密码
        if i == 3:
            child.sendline(password)
        # 生成key的文件
        if i == 4:
            child.sendline('')
        # 输入passphrase
        if i == 5:
            child.sendline('')
        # 再次输入passphrase
        if i == 6:
            child.sendline('')
        # 覆盖key文件
        if i == 7:
            child.sendline('n')
        # 密码出错
        if i == 8:
            print 'Host %s password error.' % host
            break
    os.system('chmod 700 ~/.ssh')


# 使用scp从指定远端机器复制公钥到本地，参数是远端机器IP，用户名，密码，主机名
def scp_pub_key_from_remote(host, username, password, hostname):
    ssh_password_error = 'Permission denied, please try again.'
    child = pexpect.spawn('scp %s@%s:~/.ssh/id_rsa.pub %s' % (username, host, hostname))
    while True:
        i = child.expect([pexpect.EOF, pexpect.TIMEOUT, 'password: ', ssh_password_error])
        # 执行完退出
        if i == 0:
            print 'Public rsa key of host %s get.' % host
            break
        # 超时退出
        if i == 1:
            print 'scp time out, error info:'
            print child.before, child.after
            break
        # 输入密码
        if i == 2:
            child.sendline(password)
        # 密码错误
        if i == 3:
            print 'Host %s password error.' % host
            break

    os.system('cat %s >> authorized_keys' % hostname)
    os.system('rm -rf %s' % hostname)


# 将生成的authorized_keys复制到指定的远端机器，参数为远端机器的主机IP，用户名，密码
def scp_auth_key_to_remote(host, username, password):
    ssh_password_error = 'Permission denied, please try again.'
    child = pexpect.spawn('scp authorized_keys %s@%s:~/.ssh/authorized_keys' % (username, host))
    while True:
        i = child.expect([pexpect.EOF, pexpect.TIMEOUT, 'password: ', ssh_password_error])
        # 执行完退出
        if i == 0:
            print 'authorized_keys of host %s put.' % host
            break
        # 超时退出
        if i == 1:
            print 'scp time out, error info:'
            print child.before, child.after
            break
        # 输入密码
        if i == 2:
            child.sendline(password)
        # 密码错误
        if i == 3:
            print 'Host %s password error.' % host
            break


# 删除指定远端机器的.ssh文件夹，参数为主机IP，用户名和密码
def delete_ssh(host, username, password):
    command = 'rm -rf ~/.ssh'
    ssh_connect = 'Are you sure you want to continue connecting'
    ssh_password_error = 'Permission denied, please try again.'
    child = pexpect.spawn('ssh -l %s %s %s' % (username, host, command))
    while True:
        i = child.expect([pexpect.EOF, pexpect.TIMEOUT, ssh_connect, 'password: ', ssh_password_error])
        # 执行完退出
        if i == 0:
            print 'Host %s .ssh delete OK.' % host
            break
        # 登录超时
        if i == 1:
            print 'ssh time out, error info:'
            print child.before, child.after
            break
        # 接收ssh新的key
        if i == 2:
            child.sendline('yes')
        # 输入密码
        if i == 3:
            child.sendline(password)
        # 密码输入错误
        if i == 4:
            print 'Host %s password error.' % host
            break


# 在主机之间建立信任关系类，初始化输入参数为主机列表、用户名、密码
class TrustMake(object):
    def __init__(self, config):
        self.hosts_map = eval(config.hosts_map)
        self.username = config.username
        self.password = config.password

    # 循环遍历主机列表，建信任关系
    def do_trust(self):
        # 遍历主机并生成秘钥，再将公钥复制到本地
        for host in self.hosts_map.keys():
            remote_gen_key(host, self.username, self.password)
            scp_pub_key_from_remote(host, self.username, self.password, self.hosts_map[host])

        # 修改authorized_keys文件的权限
        os.system('chmod 600 authorized_keys')

        # 遍历主机并复制authorized_keys文件
        for host in self.hosts_map.keys():
            scp_auth_key_to_remote(host, self.username, self.password)
        os.system('rm -rf authorized_keys')

    def do_delete(self):
        for host in self.hosts_map.keys():
            delete_ssh(host, self.username, self.password)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="path of config file")
    args = parser.parse_args()

    conf_object = TrustConf(args.config)
    trust_object = TrustMake(conf_object)
    trust_object.do_delete()
    trust_object.do_trust()


if __name__ == '__main__':
    main()
