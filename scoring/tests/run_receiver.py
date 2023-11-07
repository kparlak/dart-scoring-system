#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   run_receiver.py
@Time    :   2023/11/04
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Runs TCP receiver of serialized data
'''

import sys
sys.path.append("../..")
import signal
import socket
import pickle
import constants

def signal_handler(sig, frame):
    client.close()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Establish connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (constants.IP_ADDRESS, constants.PORT)
client.connect(server_address)

try:
    data = client.recv(constants.BUFFER_SIZE)
    constants.MSG = pickle.loads(data)
    print("Data received")

    for k, v in constants.MSG.items():
        print(k, v)

except Exception as e:
    print(e)
    client.close()

client.close()

# EOF
