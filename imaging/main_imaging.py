#!/usr/bin/env python

import sys
sys.path.append("..")
import constants
import socket
import time

from imaging.dartboard import Dartboard
from imaging.detection_model import DetectionModel

class ImagingStateMachine:
    def __init__(self) -> None:
        self.state = 'IDLE_START'
        self.transitions = {
            'IDLE_START' : {'start' : 'WAIT_THROW'},
            'WAIT_THROW' : {'new_dart' : 'FIND_DART'},
            'FIND_DART' : {'dart_found' : 'MAP_DART'},
            'MAP_DART' : {'done' : 'WAIT_THROW'}
        }
        self.model = DetectionModel()
        self.board = Dartboard()
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

    def runState(self):
        if self.state == 'IDLE_START':
            self.idle_start()
        elif self.state == 'WAIT_THROW':
            self.wait_throw()
        elif self.state == 'FIND_DART':
            self.find_dart()
        elif self.state == 'MAP_DART':
            self.map_dart()

    def idle_start(self):
        print("IDLE START")
        # Detect bull
        x0, y0 = self.model.find_bull()
        # Set dartboard center
        self.dartboard.set_center(x=x0, y=y0)
        # Send message to scoring system
        self.client.send(constants.READY_MSG.encode())
        # Set transition
        self.action = 'start'

    def wait_throw(self):
        print("WAIT THROW")
        while True:
            msg = self.client.recv(constants.BUFFER_SIZE).decode()
            if msg == constants.LOOK_MSG:
                break
            else:
                time.sleep(1)
        # Set transition
        self.action = 'new_dart'

    def find_dart(self):
        print("FIND DART")
        # Detect dart
        self.x, self.y = self.model.find_dart()
        # Set transition
        self.action = 'dart_found'

    def map_dart(self):
        print("MAP DART")
        # Update dartboard
        number, ring = self.board.update(x=self.x, y=self.y)
        # TODO : Send ring and number to scoring system
        #constants.MSG["radius"] = self.dartboard.get_radius()
        #constants.MSG["angle"] = self.dartboard.get_theta()
        #client.sendall(pickle.dumps(constants.MSG))
        #data = json.dumps(constants.MSG)
        #server.sendall(bytes(data, encoding="utf-8"))
        self.client.send(constants.TEST_MSG.encode())
        # Set transition
        self.action = 'done'

if __name__ == '__main__':
    SM = ImagingStateMachine()
    while True:
        SM.runState()
        SM.transition(action=SM.get_action())

# EOF
