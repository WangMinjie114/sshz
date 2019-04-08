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
import subprocess, time
import getpass


obj_path = os.path.dirname(os.path.realpath(sys.argv[0]))
print(obj_path)
obj_ip_list_path = obj_path + "/file/ip_list"
obj_host_mess_path = obj_path + "/file/host_mess"
obj_ssh_temp_path = obj_path + "/script/ssh_template.sh"
# variable
key_file = "$HOME/.ssh/id_rsa"

def read_ip_list(ip):
    '''

    :param ip: ip address
    :return:
        [0, username, port, pass]
        [1,]
    '''
    f = open(obj_ip_list_path)
    data = f.readlines()
    f.close()
    for i in data:
        if i.replace("\n", "") == ip:
            f = open(obj_host_mess_path)
            all_hosts = f.readlines()
            f.close()
            for j in all_hosts:
                if j.split(' @ ')[0] == ip:
                    host = j.replace('\n', '').split(' @ ')
                    return [0, host[1], int(host[3]), host[2], bool(host[4])]
    return [1, ]

def write_msg_file(ip, username, password, port, is_key):
    """
    ip_list is the ip
    host_mess is the host list
    :param ip:
    :param username:
    :param password:
    :param port:
    :param is_key:
    :return:
    """
    f = open(obj_ip_list_path)
    data = f.read()
    f.close()
    if ip in data:
        # update mess
        pass
    else:
        f = open(obj_ip_list_path, "a")
        f.write(ip)
        f.write('\n')
        f.close()
        host = [ip, username, password, str(port), str(is_key)]
        f = open(obj_host_mess_path, "a")
        f.write(" @ ".join(host))
        f.write('\n')
        f.close()

def connect_test(ip, username = "root", password = "", port = 22, key_file = key_file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if password == '':
            # use key
            ret = ssh.connect(hostname=ip, username=username, port=port, key_filename=key_file)
        else:
            # use password
            ret = ssh.connect(hostname=ip, username=username, port=port, password=password)
            ssh.exec_command('bash')
        return 0
    except Exception as e:
        print(e)
        return 1

def connect(ip, username = "root", password = "", port = 22, key_file = key_file, arvgs = ""):
    if sys.platform == "darwin" or sys.platform == "linux2":
        if password != "":
            f = open(obj_ssh_temp_path)
            data = f.readlines()
            f.close()
            # print(data)
            script_name = "ssh_{0}_{1}.sh".format(ip, time.time())
            f = open(script_name, "w")
            for i in data:
                if "PORT IPADDR ARGVS" in i:
                    i = i.replace("USERNAME", username).replace("IPADDR", ip).replace("ARGVS", arvgs).replace("PORT", str(port))
                if "PASSWORD" in i:
                    i = i.replace("PASSWORD", password)
                f.write(i)
            f.close()
            # print("write_success, file name {0}".format(script_name))
            request = subprocess.check_call("expect {0}".format(script_name), shell=True)
            os.remove(script_name)
            # print(request)
            if request == 0:
                write_msg_file(ip=ip, username=username, password=password, port=port, is_key=False)
        else:
            request = subprocess.check_call("ssh {1}@{0} -p {2} -i {3} {4}".format(ip, username, port, key_file, arvgs), shell=True)
            if request == 0:
                write_msg_file(ip=ip, username=username, password="", port=port, is_key=True)
    else:
        # for windows
        pass

def main(ipadd, argvs = []):
    ssh_arvgs = []
    request = read_ip_list(ipadd)
    # print(request)
    if request[0] == 0:
        # connect to hosts
        connect(ip=ipadd, username=request[1], password=request[3], port=request[2], arvgs=" ".join(argvs))
    elif request[0] == 1:
        if len(argvs) == 0:
            # 交互式获取用户名密码，用 22 端口尝试，若端口不通，则交互获取端口
            username = input("username: ")
            password = getpass.getpass("password: ")
            ret = connect_test(ip=ipadd, username=username, password=password)
            if ret == 0:
                write_msg_file(ip=ipadd, username=username, password=password, port=22, is_key=False)
                connect(ip=ipadd, username=username, password=password)
            else:
                ssh_port = int(input("port: "))
                ret1 = connect_test(ip=ipadd, username=username, password=password, port=ssh_port)
                if ret1 == 0:
                    write_msg_file(ip=ipadd, username=username, password=password, port=ssh_port, is_key=False)
                    connect(ip=ipadd, username=username, password=password, port=ssh_port, arvgs=" ".join(argvs))
                else:
                    print("connect error")
        else:
            # init variable
            ssh_username = "root"
            ssh_port = 22
            ssh_passwd = ""
            for i in argvs:
                if i == "-l":
                    count = argvs.index(i)
                    ssh_username = argvs[int(count) + 1]
                    argvs.remove(ssh_username)
                elif i == "-p":
                    count = argvs.index(i)
                    ssh_port = argvs[int(count) + 1]
                    argvs.remove(ssh_port)
                elif i == "-P":
                    count = argvs.index(i)
                    ssh_passwd = argvs[int(count) + 1]
                    argvs.remove(ssh_passwd)
                elif "-l" in i[:2]:
                    ssh_username = i[2:]
                elif "-p" in i[:2]:
                    ssh_port = i[2:]
                elif "-P" in i[:2]:
                    ssh_passwd = i[2:]
                else:
                    ssh_arvgs.append(i)
            connect(ip=ipadd, username=ssh_username, port=ssh_port, password=ssh_passwd, arvgs=" ".join(ssh_arvgs))
    else:
        pass

def env_init():
    # 创建服务器信息文件
    f = open(obj_ip_list_path, "w")
    f.close()
    f = open(obj_host_mess_path, "w")
    f.close()
    # 确认 ssh 模板脚本
    if os.path.exists(obj_ssh_temp_path):
        template = """#!/usr/bin/expect\n
set timeout 30\n
spawn ssh -l USERNAME -p PORT IPADDR ARGVS\n
expect "assword:"\n
send "PASSWORD\r"\n
interact\n
        """
        f = open(obj_ssh_temp_path, "w")
        f.write(template)
        f.close()
    # 检测依赖环境
    if sys.platform == 'linux2':
        request = subprocess.check_call("expect -c 'uptime'", shell=True)
        if request != 0:
            # 安装
            pass


if __name__ == '__main__':
    if os.path.exists(obj_ip_list_path) and os.path.exists(obj_host_mess_path):
        pass
    else:
        env_init()
    if len(sys.argv) == 1:
        print('help')
    elif len(sys.argv) == 2:
        if sys.argv[1] == "init":
            env_init()
        else:
            ipadd = sys.argv[1]
            main(ipadd)
    else:
        ipadd = sys.argv[1]
        argvs = sys.argv[2:]
        main(ipadd, argvs)
