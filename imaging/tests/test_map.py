#!/usr/bin/env python
# test_map.py

import sys
sys.path.append("..")
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
import time
import math
import numpy as np

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
    if rad >= 162 and rad < 170:
        return 'A'
    elif rad >= 107 and rad < 162:
        return 'B'
    elif rad >= 99 and rad < 107:
        return 'C'
    elif rad >= 16 and rad < 99:
        return 'D'
    elif rad >= 6.35 and rad < 16:
        return 'X'
    elif rad >= 0 and rad < 6.35:
        return 'XX'
    else:
        return 'Z'

def map_number(ang):
    if (ang >= 351 and ang <= 360) or (ang >= 0 and ang < 9):
        return 20
    elif ang >= 9 and ang < 27:
        return 5
    elif ang >= 27 and ang < 45:
        return 12
    elif ang >= 45 and ang < 63:
        return 9
    elif ang >= 63 and ang < 81:
        return 14
    elif ang >= 81 and ang < 99:
        return 11
    elif ang >= 99 and ang < 117:
        return 8
    elif ang >= 117 and ang < 135:
        return 16
    elif ang >= 135 and ang < 153:
        return 7
    elif ang >= 153 and ang < 171:
        return 19
    elif ang >= 171 and ang < 189:
        return 3
    elif ang >= 189 and ang < 207:
        return 17
    elif ang >= 207 and ang < 225:
        return 2
    elif ang >= 225 and ang < 243:
        return 15
    elif ang >= 243 and ang < 261:
        return 10
    elif ang >= 261 and ang < 279:
        return 6
    elif ang >= 279 and ang < 297:
        return 13
    elif ang >= 297 and ang < 315:
        return 4
    elif ang >= 315 and ang < 333:
        return 18
    elif ang >= 333 and ang < 351:
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
    #x_prime, y_prime = translate_pos(X, Y)
    H = np.array([[1.00243107e+00, 2.98250358e-01, -2.62532023e+02],
                [1.29748450e-07, 1.72156056e+00, 1.88249310e+02],
                [2.14034569e-10, 6.54323960e-04, 1.00000000e+00]])
    center = np.array([X0, Y0, 1])
    new_center = np.dot(H, center)
    new_center = new_center/new_center[2]
    #X0 = X0
    Y0 = new_center[1]

    point = np.array([X, Y, 1])
    new_point = np.dot(H, point)
    new_point = new_point/new_point[2]
    x_prime = X
    y_prime = new_point[1]
    #y_prime = Y

    # Fudge factor - 60 pixels length is for 1 inch from center (25.4 mm)
    factor = 25.4/60  # mm/pixel

    x_prime = x_prime * factor
    y_prime = y_prime * factor
    X0 = X0 * factor
    Y0 = Y0 * factor
    # Compute radius
    r = math.sqrt(math.pow((x_prime - X0), 2) + math.pow((y_prime - Y0), 2))
    print('r = ' + str(r))

    # Map ring hit
    ring = map_ring(rad=r)
    print('ring = ' + str(ring))

    # Compute angle
    quad_x = x_prime - X0
    quad_y = Y0 - y_prime
    print('quad_x = ' + str(quad_x))
    print('quad_y = ' + str(quad_y))

    # Compute quadrant for angle calculation
    if quad_x > 0 and quad_y > 0:  # Quadrant 1
        theta = math.atan(abs(quad_y) / abs(quad_x))
    elif quad_x < 0 and quad_y > 0:  # Quadrant 2
        theta = math.atan(abs(quad_x) / abs(quad_y)) + math.pi / 2
    elif quad_x < 0 and quad_y < 0:  # Quadrant 3
        theta = math.atan(abs(quad_y) / abs(quad_x)) + math.pi
    elif quad_x > 0 and quad_y < 0:  # Quadrant 4
        theta = math.atan(abs(quad_x) / abs(quad_y)) + 3 * math.pi / 2
    else:
        theta = 0.0
    # Convert to degrees
    theta = math.degrees(theta)
    print('theta = ' + str(theta))

    # Map number hit
    number = map_number(ang=theta)
    print('number = ' + str(number))

    print()

    time.sleep(0.1)



# EOF
