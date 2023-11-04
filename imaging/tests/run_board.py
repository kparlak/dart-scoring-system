#!/usr/bin/env python

import sys
sys.path.append("..")
import time

from detection_model import DetectionModel
from dartboard import Dartboard

model = DetectionModel(display=True)
board = Dartboard()

bull_found = False

while model.get_display().IsStreaming():
    img = model.get_source().Capture()

    if img is None:
        continue

    detections = model.get_network().Detect(img)

    model.get_display().Render(img)
    model.get_display().SetStatus("Object Detection | Network {:.0f} FPS".format(model.get_network().GetNetworkFPS()))

    for detection in detections:
        if detection.ClassID == 1 and bull_found == False: # Bull
            X0 = detection.Center[0]
            Y0 = detection.Center[1]
            board.set_center(X0, Y0)
            bull_found = True
        if detection.ClassID == 2 and bull_found == True: # Dart
            X = detection.Left
            Y = detection.Bottom

            number, ring = board.update(x=X, y=Y)
            print('number = ' + str(number))
            print('ring = ' + str(ring))
            #center_x, center_y = board.get_center()
            #print('center_x = ' + str(center_x))
            #print('center_y = ' + str(center_y))
            #pos_x, pos_y = board.get_pos()
            #print('pos_x = ' + str(pos_x))
            #print('pos_y = ' + str(pos_y))
            dist_x, dist_y = board.get_dist()
            print('dist_x = ' + str(dist_x))
            print('dist_y = ' + str(dist_y))
            theta = board.get_theta()
            print('theta = ' + str(theta))
            radius = board.get_radius()
            print('radius = ' + str(radius))
            print()

    time.sleep(0.1)

# EOF
