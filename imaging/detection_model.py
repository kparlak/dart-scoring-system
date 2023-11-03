import os
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

class DetectionModel():
    def __init__(self) -> None:
        self.source = videoSource('/dev/video0')
        self.display = videoOutput("display://0")
        self.directory = os.environ['MODEL']
        self.network = detectNet(argv=["--model=" + self.directory+ "/ssd-mobilenet.onnx",
                                       "--labels=" + self.directory  + "/labels.txt",
                                       "--input-blob=input_0",
                                       "--output-cvg=scores",
                                       "--output-bbox=boxes"], threshold=0.5)

    def get_source(self):
        return self.source

    def get_display(self):
        return self.display

    def get_network(self):
        return self.network

    def find_bull(self):
        while True:
            img = self.source.Capture()

            if img is None:
                continue

            detections = self.network.Detect(img)

            for detection in detections:
                if detection.ClassID == 1:
                    return detection.Center[0], detection.Center[1]

    def find_dart(self):
        while True:
            img = self.source.Capture()

            if img is None:
                continue

            detections = self.network.Detect(img)

            for detection in detections:
                if detection.ClassID == 2:
                    return detection.Left, detection.Right

# EOF
