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
import pickle
import struct

d0 = 431.8  # mm

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to scoring system
server_address = (constants.IMAGING_IP_ADDRESS, constants.PORT)
server.bind(server_address)
server.listen(1)  # One connection allowed
print("Waiting for scoring system to connect...")
client, address = server.accept()


CAMERA = videoSource('/dev/video0')

DIR = "/home/kevin/Documents/jetson-inference/python/training/detection/ssd/models/darts/base"

NETWORK = detectNet(argv=["--model=" + DIR + "/ssd-mobilenet.onnx",
                          "--labels=" + DIR + "/labels.txt",
                          "--input-blob=input_0",
                          "--output-cvg=scores",
                          "--output-bbox=boxes"], threshold=0.5)
X0 = 0
Y0 = 0

def detect(cam, net, id):
    while True:
        img = cam.Capture()

        if img is None:
            continue

        detections = net.Detect(img)

        for detection in detections:
            if id == 1 and detection.ClassID == 1:
                return detection.Center[0], detection.Center[1]
            elif id == 2 and detection.ClassID == 2:
                return detection.Left, detection.Bottom

def idle_start():
    print("IDLE START State")
    # Detect bull
    X0, Y0 = detect(cam=CAMERA, net=NETWORK, id=1)

    # Send ready message to scoring system
    client.send(constants.READY_MSG.encode())

def wait_throw():
    print("WAIT THROW State")
    while True:
        msg = client.recv(constants.BUFFER_SIZE).decode()
        if msg == constants.LOOK_MSG:
            break
        else:
            time.sleep(1)

def find_dart():
    print("FIND DART State")
    # Detect dart
    X, Y = detect(cam=CAMERA, net=NETWORK, id=2)
    return X, Y

def translate_pos(pixel_x, pixel_y):
    x_prime = pixel_x
    p0 = Y0
    dy = p0 / d0 * pixel_y
    y_prime = dy - d0
    return x_prime, y_prime

def map_ring(rad):
    if rad >= 162 or rad < 170:
        return 'A'
    elif rad >= 107 or rad < 162:
        return 'B'
    elif rad >= 99 or rad < 107:
        return 'C'
    elif rad >= 16 or rad < 99:
        return 'D'
    elif rad >= 6.35 or rad < 16:
        return 'X'
    elif rad >= 0 or rad < 6.35:
        return 'XX'
    else:
        return 'Z'

def map_number(ang):
    if ang >= 351 or ang < 9:
        return 20
    elif ang >= 9 or ang < 27:
        return 5
    elif ang >= 27 or ang < 45:
        return 12
    elif ang >= 45 or ang < 63:
        return 9
    elif ang >= 63 or ang < 81:
        return 14
    elif ang >= 81 or ang < 99:
        return 11
    elif ang >= 99 or ang < 117:
        return 8
    elif ang >= 117 or ang < 135:
        return 16
    elif ang >= 135 or ang < 153:
        return 7
    elif ang >= 153 or ang < 171:
        return 19
    elif ang >= 171 or ang < 189:
        return 3
    elif ang >= 189 or ang < 207:
        return 17
    elif ang >= 207 or ang < 225:
        return 2
    elif ang >= 225 or ang < 243:
        return 15
    elif ang >= 243 or ang < 261:
        return 10
    elif ang >= 261 or ang < 279:
        return 6
    elif ang >= 279 or ang < 297:
        return 13
    elif ang >= 297 or ang < 315:
        return 4
    elif ang >= 315 or ang < 333:
        return 18
    elif ang >= 333 or ang < 351:
        return 1
    else:
        return 0

def map_dart(x, y):
    print("MAP DART State")

    # Translate position
    x_prime, y_prime = translate_pos(pixel_x=x, pixel_y=y)

    # Compute radius
    r = math.sqrt(math.pow((x_prime - X0), 2) + math.pow((y_prime - Y0), 2))

    # Map ring hit
    ring = map_ring(rad=r)

    # Compute angle
    quad_x = x_prime - X0
    quad_y = y_prime - Y0

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

    # Convert to degrees
    theta = math.degrees(theta)
    # Map number hit
    number = map_number(ang=theta)

    # TODO : Send ring and number to scoring system


    print(str(number) + '-' + str(ring))

# Main loop
def main():

    idle_start()

    wait_throw()

    pixel_x, pixel_y = find_dart()

    # Map dart state
    map_dart(x=pixel_x, y=pixel_y)

    print("Done")

    server.close()

main()