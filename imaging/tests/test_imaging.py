

# ==============================================================================
# Imports
# ==============================================================================
import unittest
import socket
import time

# Client
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('10.0.0.3', 5000)

START_MSG = "START"

c.connect(server_address)

print("Client connected")

while True:
    data = c.recv(1024).decode()
    if (data == "READY"):
        break;
    time.sleep(1)

print("Sending START message")

c.send(START_MSG.encode())


print("Done")
c.close()
