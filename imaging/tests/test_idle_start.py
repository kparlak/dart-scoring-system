#!/usr/bin/env python

import sys
sys.path.append("..")
import imaging_constants as ic
from jetson_inference import detectNet
from jetson_utils import videoSource

from idle_start import idle_start

x, y = idle_start(ic.CAMERA, ic.NETWORK)

print("X = " + str(x) + ", Y = " + str(y))

# EOF
