#!/usr/bin/env python

import sys
sys.path.append("..")
from jetson_utils import videoOutput

import imaging_constants as ic

DISPLAY = videoOutput("display://0")

while DISPLAY.IsStreaming():
    img = ic.CAMERA.Capture()

    if img is None:
        continue

    detections = ic.NETWORK.Detect(img)
    
    DISPLAY.Render(img)
    DISPLAY.SetStatus("Object Detection | Network {:.0f} FPS".format(ic.NETWORK.GetNetworkFPS()))

    for detection in detections:
        if detection.ClassID == 1:  # Bull
            center_x = detection.Center[0]
            center_y = detection.Center[1]
            left = detection.Left
            right = detection.Right
            bottom = detection.Bottom
            top = detection.Top
            print("Bull: Left = " + str(left) + ", Right = " + str(right) +
                  ", Bottom = " + str(bottom) + ", Top = " + str(top))
        elif detection.ClassID == 2:  # Dart
            left = detection.Left
            right = detection.Right
            bottom = detection.Bottom
            top = detection.Top
            print("Dart: Left = " + str(left) + ", Right = " + str(right) +
                  ", Bottom = " + str(bottom) + ", Top = " + str(top))
# EOF
