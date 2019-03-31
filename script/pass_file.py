#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/29 4:54 PM
# @Author  : Wangmj
# @File    : pass_file.py
# @Note    :

import sys
import random
import os


def gen_key():
    c = list(range(256))
    random.shuffle(c)
    return c


def save_keyfile(k, f):
    fo = open(f, 'wb')
    fo.write(bytes(k))
    fo.close()


def get_key(f):
    fi = open(f, 'rb')
    k = fi.read()
    fi.close()
    return k


def crypt_file(fi, fo, key_file):
    k = get_key(key_file)
    f = open(fi, 'rb')
    fc = f.read()
    fe = open(fo, 'wb')
    flen = len(fc)
    buff = []
    for i in range(flen):
        c = i % len(k)
        fo = fc[i] ^ k[c]
        buff.append(fo)
    fe.write(bytes(buff))
    f.close()
    fe.close()


def crypt_dir(d, key_file):
    """
    encrypt a directory assigned by <d>
    """
    file_list = os.listdir(d)
    file_count = len(file_list)
    for i in range(file_count):
        f = os.path.join(d, file_list[i])
        neof = f + '.crypt'
        crypt_file(f, neof, key_file)
        print('Progress:%d/%d' % (i + 1, file_count))
    print('Directory <%s> has been encrypted/decrypted.' % (d))

def envcheck():
    '''
    check os have sshpass and ssh
    ssh -V
    sshpass
    if $? != 0; print('error')
    :return:
    '''
    pass

if __name__ == '__main__':
    envcheck()
    args = sys.argv
    arg_num = len(args)

    if arg_num == 2:
        neokey = gen_key()
        save_keyfile(neokey, args[1])
        print('Key file has been generated:%s' % (args[1]))
        exit(0)

    if arg_num == 3:
        crypt_dir(args[1], args[2])
        exit(0)

    if len(args) != 4:
        print('Usage:crypt.py <input file> <output file> <key file>')
        exit(-1)
    crypt_file(args[1], args[2], args[3])
    print('Done!')