#!/usr/bin/env python
#-*- coding: utf-8 -*-

import paramiko
import threading
import Queue

q = Queue.Queue()

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
        q.put({'ip':ip,'flow':(ReceiveBytes,TransmitBytes)})
        ssh.close()
    except :
        print '%s\tError'%(ip)

if __name__=='__main__':
    ipList=['192.168.1.55','192.168.1.100','192.168.1.101','192.168.1.200','192.168.1.201']
    username = "root"  #用户名
    passwd = ""    #密码
    result = []
    print '\nIP\t\tRX(G)\tTX(G)'
    for ip in ipList:
        th=threading.Thread(target=traffic,args=(ip,username,passwd))
        th.start()
        th.join()
    
    while not q.empty():
        result.append(q.get())

    def record(ip):
        for item in result:
            if ip == item['ip']:
                return item

    trafficResults=map(record, ipList)
    
    for item in trafficResults:
        print '%s\t%s\t%s'%(item['ip'],item['flow'][0],item['flow'][1])
    print '\n'
