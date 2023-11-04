#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   run_remote.py
@Time    :   2023/11/04
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Runs through main logic remotely
'''

import sys
sys.path.append("../..")
import constants
import socket
import time
import os
import pickle

# Create connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (constants.IP_ADDRESS, constants.PORT)
client.connect(server_address)

print("Waiting on READY message")
while True:
    data = client.recv(constants.BUFFER_SIZE).decode()
    if (data == constants.READY_MSG):
        print("Received READY message")
        break;
    else:
        time.sleep(1)

while True:
    os.system('pause')
    print("Sending LOOK message")
    client.send(constants.LOOK_MSG.encode())

    print("Waiting on dart location")
    while True:
        data = client.recv(constants.BUFFER_SIZE)
        constants.MSG = pickle.loads(data)
        for k, v in constants.MSG.items():
            print(k, v)
        # data = client.recv(1024).decode()
        # if (data == constants.TEST_MSG):
        #     break;
        break

    print()

# EOF
