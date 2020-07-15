#!/usr/bin/env python
# -*- coding: utf-8 -*-

import localinstall

INSTALL_PROMPT_ZH = '''数据层安装,请选择需要执行的操作:
    1.  设置内核参数
    2.  设置ulimit参数
    3.  安装数据层软件依赖包(GCC5.2版本)
    4.  打开防火墙端口
    5.  配置主机名
    6.  安装云管控Agent
    7.  创建编译环境(GCC5.2版本)
    8.  安装NATS集群
    9. 安装Redis集群
    10. 安装排重MDB
    11. 安装资料路由MDB
    12. 安装资料数据MDB
    0.  退出安装\n'''


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
                    pass    # TODO
            else:
                print '错误的输入,选项范围[0, 13]'
        else:
            print '错误的输入,请输入数字类型'


if __name__ == '__main__':
    main()
