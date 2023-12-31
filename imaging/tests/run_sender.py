#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   run_sender.py
@Time    :   2023/11/04
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Runs TCP sender of serialized data
'''

import sys
sys.path.append("../..")
import signal
import socket
import pickle

import constants

def signal_handler(sig, frame):
    server.close()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Create connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (constants.IP_ADDRESS, constants.PORT)
server.bind(server_address)
server.listen(constants.NUM_CONNECTIONS)
print('Waiting for connection...')
client, address = server.accept()

constants.MSG["number"] = 20
constants.MSG["ring"] = 'A'
constants.MSG["radius"] = 100.0
constants.MSG["theta"] = 45.5

try:
    data = pickle.dumps(constants.MSG, protocol=2)
    client.sendall(data)
    print("Data sent")

except Exception as e:
    print(e)
    server.close()

server.close()

# EOF
