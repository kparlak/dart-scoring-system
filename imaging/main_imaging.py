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
import constants
import socket
import time
import pickle

from dartboard import Dartboard
from model import Model

class ImagingStateMachine:
    def __init__(self) -> None:
        self.state = 'IDLE_START'
        self.transitions = {
            'IDLE_START' : {'started' : 'WAIT_THROW'},
            'WAIT_THROW' : {'thrown' : 'FIND_DART'},
            'FIND_DART' : {'found' : 'MAP_DART'},
            'MAP_DART' : {'mapped' : 'WAIT_THROW'}
        }
        self.model = Model(display=False)
        self.dartboard = Dartboard()
        self.connect()

    def connect(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (constants.IP_ADDRESS, constants.PORT)
        self.server.bind(self.server_address)
        self.server.listen(constants.NUM_CONNECTIONS)
        print('Waiting for connection...')
        self.client, self.address = self.server.accept()

    def get_action(self):
        return self.action

    def transition(self, action):
        if action in self.transitions[self.state]:
            self.state = self.transitions[self.state][action]

    def run_state(self):
        if self.state == 'IDLE_START':
            self.idle_start()
        elif self.state == 'WAIT_THROW':
            self.wait_throw()
        elif self.state == 'FIND_DART':
            self.find_dart()
        elif self.state == 'MAP_DART':
            self.map_dart()

    def idle_start(self):
        print(self.state)
        # Detect bull
        x0, y0 = self.model.find_bull()
        # Set dartboard center
        self.dartboard.set_center(x=x0, y=y0)
        # Send message to scoring system
        self.client.send(constants.READY_MSG.encode())
        # Set transition
        self.action = 'started'

    def wait_throw(self):
        print(self.state)
        # Wait for LOOK message
        while True:
            msg = self.client.recv(constants.BUFFER_SIZE).decode()
            if msg == constants.LOOK_MSG:
                break
            else:
                time.sleep(1)
        # Set transition
        self.action = 'thrown'

    def find_dart(self):
        print(self.state)
        # Detect dart
        self.x, self.y = self.model.find_dart()
        # Set transition
        self.action = 'found'

    def map_dart(self):
        print(self.state)
        # Update dartboard
        number, ring = self.dartboard.update(x=self.x, y=self.y)
        # Send data
        constants.MSG["number"] = number
        constants.MSG["ring"] = ring
        constants.MSG["radius"] = self.dartboard.get_radius()
        constants.MSG["theta"] = self.dartboard.get_theta()
        data = pickle.dumps(constants.MSG, protocol=2)
        self.client.sendall(data)
        # self.client.send(constants.TEST_MSG.encode())
        # Set transition
        self.action = 'mapped'

if __name__ == '__main__':
    try:
        state_machine = ImagingStateMachine()
        while True:
            state_machine.run_state()
            state_machine.transition(action=state_machine.get_action())

    except Exception as e:
        print(e)

# EOF
