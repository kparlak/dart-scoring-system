#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   run_main.py
@Time    :   2023/11/04
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Runs as surrogate scoring system to simulate imaging state machine logic
'''

import sys
sys.path.append("../..")
import constants
import socket
import pickle

while True:
    input('Press enter to connect...')
    # Create connection
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (constants.IP_ADDRESS, constants.PORT)
    client.connect(server_address)

    print("Waiting on READY message")
    data = client.recv(constants.BUFFER_SIZE).decode()
    if data == constants.READY_MSG:
        print('Received READY message')
    else:
        pass

    while True:
        option = int(input('Send LOOK message (1), send DONE message (2) '))
        if option == 1:
            client.send(constants.LOOK_MSG.encode())
            print("Sent LOOK message")
        elif option == 2:
            client.send(constants.DONE_MSG.encode())
            client.close()
            print("Sent DONE message")
            break

        print("Waiting on LOCATION message")
        data = client.recv(constants.BUFFER_SIZE)
        constants.MSG = pickle.loads(data)
        print(constants.MSG)

# EOF
