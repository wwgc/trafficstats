#!/usr/bin/env python
#-*- coding: utf-8 -*-

import paramiko
import threading

def traffic(ip,username,passwd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=5)
        stdin, stdout, stderr = ssh.exec_command('cat /proc/net/dev')
        out = stdout.readlines()
        conn = out[2].split()
        ReceiveBytes = round(float(conn[1])/(10**9),1)
        TransmitBytes = round(float(conn[9])/(10**9),1)
        print '%s\t%s\t%s'%(ip,ReceiveBytes,TransmitBytes)
        ssh.close()
    except :
        print '%s\tError'%(ip)

if __name__=='__main__':
    ip_list=['192.168.1.55','192.168.1.100','192.168.1.101','192.168.1.200','192.168.1.201']
    username = "root"  #用户名
    passwd = ""    #密码
    result = []
    print '\nIP\t\tRX(G)\tTX(G)'
    for ip in ip_list:
        th=threading.Thread(target=traffic,args=(ip,username,passwd))
        th.start()
        th.join()
    print '\n'