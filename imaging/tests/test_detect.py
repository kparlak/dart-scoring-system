#!/usr/bin/env python
# test_detect.py

import sys
sys.path.append("..")
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

display = videoOutput("display://0")
camera = videoSource('/dev/video0')

dir = "/home/kevin/Documents/dart-scoring-system/imaging/models/ssd"
network = detectNet(argv=["--model=" + dir + "/ssd-mobilenet.onnx",
                          "--labels=" + dir + "/labels.txt",
                          "--input-blob=input_0",
                          "--output-cvg=scores",
                          "--output-bbox=boxes"], threshold=0.5)

while display.IsStreaming():
    img = camera.Capture()

    if img is None:
        continue

    detections = network.Detect(img)

    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(network.GetNetworkFPS()))

    for detection in detections:
        if detection.ClassID == 1:  # Bull
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
