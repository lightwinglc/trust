#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import os
import ConfigParser
import pexpect
 
#配置文件类，从配置文件中获取主机列表、用户名和密码，初始化输入参数为配置文件路径
class TrustConf(object):
    def __init__(self, file):
        self.file = file
        self.parseConf()
 
    def parseConf(self):
        config = ConfigParser.ConfigParser()
        with open(self.file, 'r') as cfgfile:
            config.readfp(cfgfile)
            self.hostsmap = config.get('hosts', 'hostsmap')
            self.username = config.get('hosts', 'username')
            self.password = config.get('hosts', 'password')
 
 
#在主机之间建立信任关系类，初始化输入参数为主机列表、用户名、密码
class TrustMake(object):
    def __init__(self, config):
        self.hostsmap = eval(config.hostsmap)
        self.username = config.username
        self.password = config.password
 
    #循环遍历主机列表，建信任关系
    def doTrust(self):
        #遍历主机并生成秘钥，再将公钥复制到本地
        for host in self.hostsmap.keys():
            self.remoteGenKey(host, self.username, self.password)
            self.scpPubKeyFromRemote(host, self.username, self.password, self.hostsmap[host])
 
        #修改authorized_keys文件的权限
        os.system('chmod 600 authorized_keys')
 
        #遍历主机并复制authorized_keys文件
        for host in self.hostsmap.keys():
            self.scpAuthKeyToRemote(host, self.username, self.password)
        os.system('rm -rf authorized_keys')
 
    def doDelete(self):
        for host in self.hostsmap.keys():
            self.deleteSSH(host, self.username, self.password)

    #在指定的主机上生成ssh秘钥，参数为主机IP，用户名和密码，已有key文件不进行覆盖
    def remoteGenKey(self, host, username, password):
        command = 'ssh-keygen -t rsa'
        ssh_newkey = 'Are you sure you want to continue connecting'
        ssh_keyfile = 'Enter file in which to save the key'
        ssh_passphrase = 'Enter passphrase'
        ssh_reputpassphrase = 'Enter same passphrase again'
        ssh_Overwrite = 'Overwrite'
        ssh_PasswdError = 'Permission denied, please try again.'
        child = pexpect.spawn('ssh -l %s %s %s'%(username, host, command))
        while True:
            i = child.expect([pexpect.EOF, pexpect.TIMEOUT, ssh_newkey, 'password: ', ssh_keyfile, ssh_passphrase, ssh_reputpassphrase, ssh_Overwrite, ssh_PasswdError])
            #执行完退出
            if i == 0:
                print 'Host %s generating public/private rsa key pair OK.'%(host)
                break
            #登录超时
            if i == 1:
                print 'ssh time out, error info:'
                print child.before, child.after
                break
            #接收ssh新的key
            if i == 2:
                child.sendline('yes')
            #输入密码
            if i == 3:
                child.sendline(password)
            #生成key的文件
            if i == 4:
                child.sendline('')
            #输入passphrase
            if i == 5:
                child.sendline('')
            #再次输入passphrase
            if i == 6:
                child.sendline('')
            #覆盖key文件
            if i == 7:
                child.sendline('n')
            #密码出错
            if i == 8:
                print 'Host %s password error.'%(host)
                break
        os.system('chmod 700 ~/.ssh')
 
    #使用scp从指定远端机器复制公钥到本地，参数是远端机器IP，用户名，密码，主机名
    def scpPubKeyFromRemote(self, host, username, password, hostname):
        ssh_PasswdError = 'Permission denied, please try again.'
        child = pexpect.spawn('scp %s@%s:~/.ssh/id_rsa.pub %s'%(username, host, hostname))
        while True:
            i = child.expect([pexpect.EOF, pexpect.TIMEOUT, 'password: ', ssh_PasswdError])
            #执行完退出
            if i == 0:
                print 'Public rsa key of host %s get.'%(host)
                break
            #超时退出
            if i == 1:
                print 'scp time out, error info:'
                print child.before, child.after
                break
            #输入密码
            if i == 2:
                child.sendline(password)
            #密码错误
            if i == 3:
                print 'Host %s password error.'%(host)
                break
 
        os.system('cat %s >> authorized_keys'%(hostname))
        os.system('rm -rf %s'%(hostname))
 
    #将生成的authorized_keys复制到指定的远端机器，参数为远端机器的主机IP，用户名，密码
    def scpAuthKeyToRemote(self, host, username, password):
        ssh_PasswdError = 'Permission denied, please try again.'
        child = pexpect.spawn('scp authorized_keys %s@%s:~/.ssh/authorized_keys'%(username, host))
        while True:
            i = child.expect([pexpect.EOF, pexpect.TIMEOUT, 'password: ', ssh_PasswdError])
            #执行完退出
            if i == 0:
                print 'authorized_keys of host %s put.'%(host)
                break
            #超时退出
            if i == 1:
                print 'scp time out, error info:'
                print child.before, child.after
                break
            #输入密码
            if i == 2:
                child.sendline(password)
            #密码错误
            if i == 3:
                print 'Host %s password error.'%(host)
                break
 
    #删除指定远端机器的.ssh文件夹，参数为主机IP，用户名和密码
    def deleteSSH(self, host, username, password):
        command = 'rm -rf ~/.ssh'
        ssh_connect = 'Are you sure you want to continue connecting'
        ssh_PasswdError = 'Permission denied, please try again.'
        child = pexpect.spawn('ssh -l %s %s %s'%(username, host, command))
        while True:
            i = child.expect([pexpect.EOF, pexpect.TIMEOUT, ssh_connect, 'password: ', ssh_PasswdError])
            #执行完退出
            if i == 0:
                print 'Host %s .ssh delete OK.'%(host)
                break
            #登录超时
            if i == 1:
                print 'ssh time out, error info:'
                print child.before, child.after
                break
            #接收ssh新的key
            if i == 2:
                child.sendline('yes')
            #输入密码
            if i == 3:
                child.sendline(password)
            #密码输入错误
            if i == 4:
                print 'Host %s password error.'%(host)
                break

if __name__ == '__main__':
    myconf = TrustConf('./trust.ini')
    mytrust = TrustMake(myconf)
    mytrust.doDelete()
    mytrust.doTrust()
