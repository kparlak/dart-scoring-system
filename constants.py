#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   constants.py
@Time    :   2023/11/04
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Constants used by imaging and scoring systems
'''

IP_ADDRESS = '10.0.0.3'
PORT = 5000
NUM_CONNECTIONS = 1

BUFFER_SIZE = 1024

READY_MSG = "READY"
LOOK_MSG = "LOOK"
TEST_MSG = "TEST"

# Data message
MSG = {"number": 0, "ring": 'A', "radius": 0.0, "theta": 0.0}

# EOF
