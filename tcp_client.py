__author__ = 'DarkWing'
#_*_ coding:utf-8 _*_

import socket

target_host = "127.0.0.1"
target_port = 9999

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect((target_host,target_port))

client.send("GET / HTTP/1.1\r\nHost:zjicmisa.org\r\n\r\n")

response = client.recv(4096)

print response