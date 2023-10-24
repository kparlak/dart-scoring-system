#!/usr/bin/env python
# test_map.py

import sys
sys.path.append("..")
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
import time
import math

display = videoOutput("display://0")
camera = videoSource('/dev/video0')

dir = "/home/kevin/Documents/dart-scoring-system/imaging/models/ssd"
network = detectNet(argv=["--model=" + dir + "/ssd-mobilenet.onnx",
                          "--labels=" + dir + "/labels.txt",
                          "--input-blob=input_0",
                          "--output-cvg=scores",
                          "--output-bbox=boxes"], threshold=0.5)

d0 = 431.8  # mm
X0 = 0
Y0 = 0
X = 0
Y = 0

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

while display.IsStreaming():
    img = camera.Capture()

    if img is None:
        continue

    detections = network.Detect(img)

    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(network.GetNetworkFPS()))

    # Find bull and dart
    for detection in detections:
        if detection.ClassID == 1:
            X0 = detection.Center[0]
            Y0 = detection.Center[1]
        else:
            X = detection.Left
            Y = detection.Bottom

    # Translate position
    x_prime, y_prime = translate_pos(X, Y)

    # Compute radius
    r = math.sqrt(math.pow((x_prime - X0), 2) + math.pow((y_prime - Y0), 2))

    # Map ring hit
    ring = map_ring(rad=r)
    # Compute angle
    quad_x = x_prime - X0
    quad_y = y_prime - Y0
    # Compute quadrant for angle calculation
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

    print(str(number) + str(ring))

    time.sleep(0.1)



# EOF
