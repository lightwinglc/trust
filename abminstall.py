#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

INSTALL_PROMPT_ZH = '''数据层安装,请选择需要执行的操作:
    1.  本地环境安装python依赖包
    2.  设置内核参数
    3.  设置ulimit参数
    4.  安装数据层软件依赖包(GCC5.2版本)
    5.  打开防火墙端口
    6.  配置主机名
    7.  安装云管控Agent
    8.  创建编译环境(GCC5.2版本)
    9.  安装NATS集群
    10. 安装Redis集群
    11. 安装排重MDB
    12. 安装资料路由MDB
    13. 安装资料数据MDB
    0.  退出安装\n'''

SETUPTOOLS_PACKAGE_NAME = 'setuptools-44.1.1.zip'
PIP_PACKAGE_NAME = 'pip-20.1.1.tar.gz'
PEXPECT_PACKAGE_NAME = 'pexpect-4.8.0-py2.py3-none-any.whl'
PTYPROCESS_PACKAGE_NAME = 'ptyprocess-0.6.0-py2.py3-none-any.whl'


# 获取脚本路径
def get_script_path(dir_name):
    current_path = os.path.abspath(__file__)
    return os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep), dir_name)


# 在本地安装python的依赖包
def install_python_package():
    # 获取包路径
    package_path = get_script_path('package')
    # 安装setuptools
    setuptools_dir_archive = os.path.join(package_path, SETUPTOOLS_PACKAGE_NAME)
    setuptools_dir = os.path.join(package_path, os.path.splitext(SETUPTOOLS_PACKAGE_NAME)[0])
    if os.path.isdir(setuptools_dir):    # 解压目录存在
        try:
            shutil.rmtree(setuptools_dir)
        except OSError, msg:
            print "删除目录 %s 失败: %s.退出..." % (setuptools_dir, str(msg))
            exit()
        else:
            print "删除目录 %s 成功" % setuptools_dir
    os.system('unzip -o %s -d %s' % (setuptools_dir_archive, package_path))
    cmd = 'python %s -d -v 2.1.1' % os.path.join(setuptools_dir, 'bootstrap.py')
    print cmd
    os.system('cd %s;python %s -d -v 2.1.1' % (setuptools_dir, os.path.join(setuptools_dir, 'bootstrap.py')))
    cmd = 'python %s install' % os.path.join(setuptools_dir, 'setup.py')
    print cmd
    os.system('python %s install' % os.path.join(setuptools_dir, 'setup.py'))


def main():
    while True:
        option = raw_input(INSTALL_PROMPT_ZH)
        if option.isdigit():
            option = int(option)
            if 0 <= option <= 13:
                print '用户输入 %d' % option
                if 0 == option:
                    print '退出安装'
                    break
                elif 1 == option:
                    install_python_package()
            else:
                print '错误的输入,选项范围[0, 13]'
        else:
            print '错误的输入,请输入数字类型'


if __name__ == '__main__':
    main()
