#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 9:52 AM
# @Author  : Wangmj
# @File    : main.py
# @Note    :

import sys
import random
import os
import re
import paramiko

def read_ip_list(ip):
    '''

    :param ip: ip address
    :return:
        [0, username, port, pass]
        [1,]
    '''
    pass

def write_msg_file():
    pass

def connect_test():
    pass

def connect(username, password, port = 22):
    pass

def main(ipadd, argvs = []):
    request = read_ip_list(ipadd)
    if request[0] == 0:
        # connect to hosts

        pass
    elif request[0] == 1:
        if len(argvs) == 0:
            # 交互式获取用户名密码，用 22 端口尝试，若端口不通，则交互获取端口
            username = input("username: ")
            password = input("password: ")
            ret = connect_test()
            if ret == 0:
                write_msg_file()
                connect(username, password)
            else:
                port = input("port: ")
                ret1 = connect_test()
                if ret1 == 0:
                    write_msg_file()
                    connect(username, password, port)
                else:
                    print("connect error")
        else:
            for i in argvs:
                if i == "-l":
                    count = argvs.index(i)
                    username = argvs[int(count) + 1]
                if
    pass

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('help')
    elif len(sys.argv) == 2:
        ipadd = sys.argv[1]
        main(ipadd)
    else:
        ipadd = sys.argv[1]
        argvs = sys.argv[2:]
        main(ipadd, argvs)
