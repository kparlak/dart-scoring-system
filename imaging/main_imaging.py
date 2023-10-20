#!/usr/bin/env python
# constants.py

import sys
sys.path.append("..")
import constants
import socket
import time
from jetson_inference import detectNet
from jetson_utils import videoSource



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to scoring system
server_address = (constants.IMAGING_IP_ADDRESS, constants.PORT)
server.bind(server_address)

server.listen(1)  # One connection allowed
print("Waiting for scoring system to connect...")
client, address = server.accept()


camera = videoSource('/dev/video0')

dir = "/home/kevin/Documents/jetson-inference/python/training/detection/ssd/models/darts/base"

net = detectNet(argv=["--model=" + dir + "/ssd-mobilenet.onnx",
                      "--labels=" + dir + "/labels.txt",
                      "--input-blob=input_0",
                      "--output-cvg=scores",
                      "--output-bbox=boxes"], threshold=0.5)

center_x = 0
center_y = 0

def idle_start():
    print("IDLE START State")
    # Wait for bull detection
    while True: # TODO : Add timeout
        img = camera.Capture()

        if img is None:
            continue

        detections = net.Detect(img)

        for detection in detections:
            if detection.ClassID == 1:
                center_x = detection.Center[0]
                center_y = detection.Center[1]
                bull_detected = True
                break

        if bull_detected == True:
            break

    # Send ready message to scoring system
    client.send(constants.READY_MSG.encode())

def wait_throw():
    print("WAIT THROW State")
    print("Waiting for start...")
    while True:
        msg = client.recv(constants.BUFFER_SIZE).decode()
        if msg == constants.THROW_MSG:
            break
        time.sleep(1)

def find_dart():
    print("FIND DART State")

def map_dart():
    print("MAP DART State")

# Main loop
def main():
    idle_start()

    wait_throw()

    find_dart()

    map_dart()

    print("Done")

    server.close()

main()