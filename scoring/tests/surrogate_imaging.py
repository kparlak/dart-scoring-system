#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   surrogate_imaging.py
@Time    :   2023/11/10
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Runs as surrogate imaging system to simulate scoring state machine logic
'''

import sys
sys.path.append("../..")
import signal
import constants
import socket
import pickle

def signal_handler(sig, frame):
    server.close()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Create connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (constants.IP_ADDRESS, constants.PORT)
server.bind(server_address)
server.listen(constants.NUM_CONNECTIONS)

while True:
    print('Waiting for connection...')
    client, address = server.accept()

    print('Sending ready message')
    client.send(constants.READY_MSG.encode())

    while True:
        data = client.recv(constants.BUFFER_SIZE).decode()
        if data == constants.LOOK_MSG:
            print('LOOK message received, sending location')
            number = int(input('Number of hit: '))
            constants.MSG["number"] = number
            ring = input('Ring of hit: ')
            constants.MSG["ring"] = ring
            data = pickle.dumps(constants.MSG, protocol=2)
            client.sendall(data)
        elif data == constants.DONE_MSG:
            print('DONE message received, disconnecting')
            break
        # else:
        #     print('Message not recognized')

# EOF
