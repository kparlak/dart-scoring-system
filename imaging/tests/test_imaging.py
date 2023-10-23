#!/usr/bin/env python
# test_imaging.py

import sys
sys.path.append("../..")
import constants
import socket
import time
import sys
import os
import pickle
import signal

def signal_handler():
    client.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Open client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
client.connect(server_address)

print("Waiting for READY message")
while True:
    data = client.recv(1024).decode()
    if (data == constants.READY_MSG):
        break
    time.sleep(1)

os.system('pause')
print("Sending LOOK message")
client.send(constants.LOOK_MSG.encode())

print("Waiting on dart location")
while True:
    data_raw = client.recv(1024)
    data = pickle.loads(data_raw)
    print(data)
    time.sleep(1)

# EOF
