#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   model.py
@Time    :   2023/11/04
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Class for model logic
'''

import os

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

class Model():
    def __init__(self, display) -> None:
        self.source = videoSource('/dev/video0')
        self.directory = os.environ['MODEL']
        self.network = detectNet(argv=["--model=" + self.directory+ "/ssd-mobilenet.onnx",
                                       "--labels=" + self.directory  + "/labels.txt",
                                       "--input-blob=input_0",
                                       "--output-cvg=scores",
                                       "--output-bbox=boxes"], threshold=0.5)
        if display == True:
            self.display = videoOutput("display://0")

    def get_source(self):
        return self.source

    def get_display(self):
        return self.display

    def get_network(self):
        return self.network

    def detect(self, id=0):
        while True:
            # Capture image
            img = self.source.Capture()
            if img is None:
                continue
            # Run image through detection network
            detections = self.network.Detect(img)
            for detection in detections:
                if detection.ClassID == id:
                    return detection

    def detect_bull(self):
        detection = self.detect(id=1)
        return detection.Center[0], detection.Center[1]

    def detect_dart(self):
        detection = self.detect(id=2)
        return detection.Left, detection.Bottom

# EOF
