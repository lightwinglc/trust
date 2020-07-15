#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pexpect


def remote_gen_key(host, username, password, port):
    command = 'ssh-keygen -t rsa'
    ssh_new_key = 'Are you sure you want to continue connecting'
    ssh_key_file = 'Enter file in which to save the key'
    ssh_passphrase = 'Enter passphrase'
    ssh_re_put_passphrase = 'Enter same passphrase again'
    ssh_over_write = 'Overwrite'
    ssh_password_error = 'Permission denied, please try again.'
    child = pexpect.spawn('ssh -l %s %s -p %s %s' % (username, host, port, command))
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
