#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   run_model.py
@Time    :   2023/11/04
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Runs through model logic
'''

import sys
sys.path.append("..")
import time

from model import Model

model = Model(display=True)

while model.get_display().IsStreaming():
    img = model.get_source().Capture()

    if img is None:
        continue

    detections = model.get_network().Detect(img)

    model.get_display().Render(img)
    model.get_display().SetStatus("Object Detection | Network {:.0f} FPS".format(model.get_network().GetNetworkFPS()))

    for detection in detections:
        left = detection.Left
        right = detection.Right
        bottom = detection.Bottom
        top = detection.Top

        if detection.ClassID == 1: # Bull
            print("BULL")
        if detection.ClassID == 2: # Dart
            print("DART")

        print("Left = " + str(left) + ", Right = " + str(right) +
              ", Bottom = " + str(bottom) + ", Top = " + str(top))

        print()

        time.sleep(0.1)

# EOF
