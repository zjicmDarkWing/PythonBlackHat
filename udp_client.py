__author__ = 'DarkWing'
#_*_ coding:utf-8 _*_

import socket

target_host = "zjicmisa.org"
target_port = 80

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

client.sendto("AAAAAABBBBCCC",(target_host,target_port))

data,addr = client.recvfrom(4096)

print data