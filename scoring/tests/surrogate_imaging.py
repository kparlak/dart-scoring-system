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
import socket
import pickle

import constants

while True:
    # Create connection
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (constants.IP_ADDRESS, constants.PORT)
    server.bind(server_address)
    server.listen(constants.NUM_CONNECTIONS)
    print("Waiting for connection...")
    client, address = server.accept()
    client.send(constants.READY_MSG.encode())
    print("Sent READY message")

    while True:
        print("Waiting on LOOK message")
        data = client.recv(constants.BUFFER_SIZE).decode()
        if data == constants.LOOK_MSG:
            number = int(input('Number of hit: '))
            constants.MSG["number"] = number
            ring = input('Ring of hit: ')
            constants.MSG["ring"] = ring
            radius = float(input('Radius of hit: '))
            constants.MSG["radius"] = radius
            theta = float(input('Theta of hit: '))
            constants.MSG["theta"] = theta
            data = pickle.dumps(constants.MSG, protocol=2)
            client.sendall(data)
            print("Sent LOCATION message")
        elif data == constants.DONE_MSG:
            print("Received DONE message, disconnecting")
            server.close()
            client.close()
            break
        else:
            pass

# EOF
