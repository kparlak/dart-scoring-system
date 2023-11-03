from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

class Detection():
    def __init__(self) -> None:
        self.source = videoSource('/dev/video0')
        self.directory = "/home/kevin/Documents/jetson-inference/python/training/detection/ssd/models/darts/base"
        self.network = detectNet(argv=["--model=" + self.directory + "/ssd-mobilenet.onnx",
                                       "--labels=" + self.directory  + "/labels.txt",
                                       "--input-blob=input_0",
                                       "--output-cvg=scores",
                                       "--output-bbox=boxes"], threshold=0.5)

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
