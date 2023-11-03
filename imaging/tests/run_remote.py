#!/usr/bin/env python

import sys
sys.path.append("..")
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
    data = client.recv(1024).decode()
    if (data == constants.READY_MSG):
        break;
    else:
        time.sleep(1)

while True:
    os.system('pause')
    print("Sending LOOK message")
    client.send(constants.LOOK_MSG.encode())

    print("Waiting on dart location")
    while True:
        # data = client.recv(1024)
        # kevin = pickle.loads(data)
        # print(data)
        # time.sleep(1)
        data = client.recv(1024).decode()
        if (data == constants.TEST_MSG):
            break;
        time.sleep(1)

# EOF
