from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

CAMERA = videoSource('/dev/video0')

DIR = "/home/kevin/Documents/jetson-inference/python/training/detection/ssd/models/darts/base"

NETWORK = detectNet(argv=["--model=" + DIR + "/ssd-mobilenet.onnx",
                          "--labels=" + DIR + "/labels.txt",
                          "--input-blob=input_0",
                          "--output-cvg=scores",
                          "--output-bbox=boxes"], threshold=0.5)

# EOF
