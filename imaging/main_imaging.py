#!/usr/bin/env python
# constants.py

import sys
sys.path.append("..")
import constants
import socket
import time
import math
from jetson_inference import detectNet
from jetson_utils import videoSource

#from idle_start import idle_start

d0 = 431.8  # mm

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
        bull_detected = False
        img = camera.Capture()

        if img is None:
            continue

        detections = net.Detect(img)

        for detection in detections:
            if detection.ClassID == 1:  # Bull
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
    while True:
        msg = client.recv(constants.BUFFER_SIZE).decode()
        if msg == constants.LOOK_MSG:
            break
        time.sleep(1)

def find_dart():
    print("FIND DART State")
    while True:
        img = camera.Capture()

        if img is None:
            continue

        detections = net.Detect(img)

        for detection in detections:
            if detection.ClassID == 2:  # Dart
                pixel_x = detection.Left
                pixel_y = detection.Bottom
                return pixel_x, pixel_y

def map_dart(x, y):
    print("MAP DART State")
    x_loc = x
    # Translate y location due to projection geometry
    p0 = center_y
    dy = p0 / d0 * y
    y_loc = dy - d0

    r = math.sqrt(math.pow((x_loc - center_x), 2) + math.pow((y_loc - center_y), 2))


    # Map ring hit
    print(str(x_loc - center_x))
    if r >= 162 or r < 170:
        print("A")
    elif r >= 107 or r < 162:
        print("B")
    elif r >= 99 or r < 107:
        print("C")
    elif r >= 16 or r < 99:
        print("D")
    elif r >= 6.35 or r < 16:
        print("X")
    elif r >= 0 or r < 6.35:
        print("XX")
    else:
        print("Z")

    # Map number hit
    quad_x = x_loc - center_x
    quad_y = y - center_y

    if quad_x > 0 and quad_y > 0:
        theta = math.atan(quad_y / quad_x)
    elif quad_x < 0 and quad_y > 0:
        theta = math.atan(quad_x / quad_y) + math.pi
    elif quad_x > 0 and quad_y < 0:
        theta = math.atan(quad_y / quad_x) + 2 * math.pi
    elif quad_x < 0 and quad_y < 0:
        theta = math.atan(quad_x / quad_y) + 3 * math.pi
    else:
        theta = 0.0

    
    theta = math.degrees(theta)
    print(str(theta))

    if theta >= 351 or theta < 9:
        number = 20
    elif theta >= 9 or theta < 27:
        number = 5
    elif theta >= 27 or theta < 45:
        number = 12
    elif theta >= 45 or theta < 63:
        number = 9
    elif theta >= 63 or theta < 81:
        number = 14
    elif theta >= 81 or theta < 99:
        number = 11
    elif theta >= 99 or theta < 117:
        number = 8
    elif theta >= 117 or theta < 135:
        number = 16
    elif theta >= 135 or theta < 153:
        number = 7
    elif theta >= 153 or theta < 171:
        number = 19
    elif theta >= 171 or theta < 189:
        number = 3
    elif theta >= 189 or theta < 207:
        number = 17
    elif theta >= 207 or theta < 225:
        number = 2
    elif theta >= 225 or theta < 243:
        number = 15
    elif theta >= 243 or theta < 261:
        number = 10
    elif theta >= 261 or theta < 279:
        number = 6
    elif theta >= 279 or theta < 297:
        number = 13
    elif theta >= 297 or theta < 315:
        number = 4
    elif theta >= 315 or theta < 333:
        number = 18
    elif theta >= 333 or theta < 351:
        number = 1
    else:
        number = 0

    print(number)

# Main loop
def main():
    # 

    idle_start()

    wait_throw()

    pixel_x, pixel_y = find_dart()

    map_dart(x=pixel_x, y=pixel_y)

    print("Done")

    server.close()

main()