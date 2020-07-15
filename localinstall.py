#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 本地环境安装python依赖包

import os
import shutil

SETUPTOOLS_PACKAGE_NAME = 'setuptools-44.1.1.zip'
PIP_PACKAGE_NAME = 'pip-18.1.zip'
PEXPECT_PACKAGE_NAME = 'pexpect-4.8.0-py2.py3-none-any.whl'
PTYPROCESS_PACKAGE_NAME = 'ptyprocess-0.6.0-py2.py3-none-any.whl'


# 获取脚本路径
def get_script_path(dir_name):
    current_path = os.path.abspath(__file__)
    return os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep), dir_name)


# 安装setuptools
def install_setuptools(package_path):
    print "准备安装 setuptools"
    setuptools_dir_archive = os.path.join(package_path, SETUPTOOLS_PACKAGE_NAME)
    setuptools_dir = os.path.join(package_path, os.path.splitext(SETUPTOOLS_PACKAGE_NAME)[0])
    if os.path.isdir(setuptools_dir):  # 解压目录存在
        print "setuptools 解压目录 %s 存在, 删除重新解压" % setuptools_dir
        try:
            shutil.rmtree(setuptools_dir)
        except OSError, msg:
            print "删除解压目录 %s 失败: %s. 退出..." % (setuptools_dir, str(msg))
            exit()
        else:
            print "删除解压目录 %s 成功" % setuptools_dir
    print "解压setuptools压缩包 %s" % setuptools_dir_archive
    os.system('unzip -q -o %s -d %s' % (setuptools_dir_archive, package_path))
    cmd = 'cd %s;python %s -d -v 2.1.1 > /dev/null 2>&1' % \
          (setuptools_dir, os.path.join(setuptools_dir, 'bootstrap.py'))
    print "执行命令: %s" % cmd
    os.system(cmd)
    cmd = 'python %s install > /dev/null 2>&1' % os.path.join(setuptools_dir, 'setup.py')
    print "执行命令: %s" % cmd
    os.system(cmd)
    print "setuptools 安装完成"


# 安装pip
def install_pip(package_path):
    print "准备安装 pip"
    pip_dir_archive = os.path.join(package_path, PIP_PACKAGE_NAME)
    pip_dir = os.path.join(package_path, os.path.splitext(PIP_PACKAGE_NAME)[0])
    if os.path.isdir(pip_dir):  # 解压目录存在
        print "pip 解压目录 %s 存在, 删除重新解压" % pip_dir
        try:
            shutil.rmtree(pip_dir)
        except OSError, msg:
            print "删除解压目录 %s 失败: %s. 退出..." % (pip_dir, str(msg))
            exit()
        else:
            print "删除解压目录 %s 成功" % pip_dir
    print "解压pip压缩包 %s" % pip_dir_archive
    os.system('unzip -q -o %s -d %s' % (pip_dir_archive, package_path))
    cmd = 'cd %s;python setup.py install > /dev/null 2>&1' % pip_dir
    print "执行命令: %s" % cmd
    os.system(cmd)
    print "pip 安装完成"


# 安装ptyprocess
def install_ptyprocess(package_path):
    print "准备安装 ptyprocess"
    cmd = 'cd %s;pip install %s' % (package_path, PTYPROCESS_PACKAGE_NAME)
    print "执行命令: %s" % cmd
    os.system(cmd)
    print "ptyprocess 安装完成"


# 安装pexpect
def install_pexpect(package_path):
    print "准备安装 pexpect"
    cmd = 'cd %s;pip install %s' % (package_path, PEXPECT_PACKAGE_NAME)
    print "执行命令: %s" % cmd
    os.system(cmd)
    print "pexpect 安装完成"


# 在本地安装python的依赖包
def install_python_package():
    # 获取包路径
    package_path = get_script_path('package')
    install_setuptools(package_path)
    install_pip(package_path)
    install_ptyprocess(package_path)
    install_pexpect(package_path)


def main():
    install_python_package()


if __name__ == '__main__':
    main()
