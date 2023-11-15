#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   main_imaging.py
@Time    :   2023/11/04
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Main for imaging system
'''

import sys
sys.path.append("..")
import socket
import pickle

import constants

from dartboard import Dartboard
from model import Model

class ImagingStateMachine:
    def __init__(self) -> None:
        self.state = 'IDLE_START'
        self.transitions = {
            # Action               Current State  Next State
            'ready_msg_txd'    : {'IDLE_START' : 'WAIT_THROW'},
            'look_msg_rxd'     : {'WAIT_THROW' : 'FIND_DART'},
            'done_msg_rxd'     : {'WAIT_THROW' : 'IDLE_START'},
            'dart_found'       : {'FIND_DART'  : 'MAP_DART'},
            'location_msg_txd' : {'MAP_DART'   : 'WAIT_THROW'}
        }
        self.model = Model(display=False)
        self.dartboard = Dartboard()

    def connect(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (constants.IP_ADDRESS, constants.PORT)
        self.server.bind(self.server_address)
        self.server.listen(constants.NUM_CONNECTIONS)
        print("Waiting for connection...")
        self.client, self.address = self.server.accept()

    def disconnect(self):
        self.server.close()
        self.client.close()

    def get_action(self):
        return self.action

    def transition(self, action):
        if action in self.transitions.keys():
            self.state = self.transitions[action][self.state]

    def run_state(self):
        if self.state == 'IDLE_START':
            self.idle_start()
        elif self.state == 'WAIT_THROW':
            self.wait_throw()
        elif self.state == 'FIND_DART':
            self.find_dart()
        elif self.state == 'MAP_DART':
            self.map_dart()
        else:
            pass

    def idle_start(self):
        print(self.state)
        # Connect to scoring system
        self.connect()
        # Detect bull
        x0, y0 = self.model.detect_bull()
        # Set dartboard center
        self.dartboard.set_center(x=x0, y=y0)
        # Send message to scoring system
        self.client.send(constants.READY_MSG.encode())
        self.action = 'ready_msg_txd'

    def wait_throw(self):
        print(self.state)
        # Wait for message from scoring system
        msg = self.client.recv(constants.BUFFER_SIZE).decode()
        if msg == constants.LOOK_MSG:
            self.action = 'look_msg_rxd'
        elif msg == constants.DONE_MSG:
            self.disconnect()
            self.action = 'done_msg_rxd'
        else:
            pass

    def find_dart(self):
        print(self.state)
        # Detect dart
        self.x, self.y = self.model.detect_dart()
        self.action = 'dart_found'

    def map_dart(self):
        print(self.state)
        # Update dartboard
        number, ring = self.dartboard.update(x=self.x, y=self.y)
        # Send message to scoring system
        constants.MSG["number"] = number
        constants.MSG["ring"] = ring
        constants.MSG["radius"] = self.dartboard.get_radius()
        constants.MSG["theta"] = self.dartboard.get_theta()
        print(constants.MSG)
        data = pickle.dumps(constants.MSG, protocol=2)
        self.client.sendall(data)
        # self.client.send(constants.TEST_MSG.encode())
        self.action = 'location_msg_txd'

if __name__ == '__main__':
    try:
        sm = ImagingStateMachine()
        while True:
            sm.run_state()
            sm.transition(action=sm.get_action())

    except Exception as e:
        print(e)

# EOF
