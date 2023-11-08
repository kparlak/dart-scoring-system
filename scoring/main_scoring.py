#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   main_scoring.py
@Time    :   2023/11/05
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Main for scoring system
'''

import sys
sys.path.append("..")
import constants
import socket
import os
import pickle

from game_501 import Game501
from game_around_the_world import GameAroundTheWorld

class ScoringStateMachine:
    def __init__(self):
        self.state = 'SELECT_GAME'
        self.transitions = {
            'SELECT_GAME' : {'game_selected' : 'IDLE_TURN'},
            'IDLE_TURN' : {'profile_selected' : 'NEW_DART'},
            'NEW_DART' : {'look_msg_txd' : 'WAIT_DART'},
            'WAIT_DART' : {'location_msg_rxd' : 'UPDATE_GAME'},
            'UPDATE_GAME' : {'winner' : 'FINISH_GAME'},
            'UPDATE_GAME' : {'no_winner' : 'IDLE_TURN'},
            'FINISH_GAME' : {'again' : 'SELECT_GAME'},
            'FINISH_GAME' : {'not_again' : 'IDLE_TURN'}
        }
        self.num_players = 0
        self.connect()

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (constants.IP_ADDRESS, constants.PORT)
        self.client.connect(server_address)

    def get_action(self):
        return self.action

    def transition(self, action):
        if action in self.transitions[self.state]:
            self.state = self.transitions[self.state][action]

    def run_state(self):
        if self.state == 'SELECT_GAME':
            self.select_game()
        elif self.state == 'IDLE_TURN':
            self.idle_turn()
        elif self.state == 'NEW_DART':
            self.new_dart()
        elif self.state == 'WAIT_DART':
            self.wait_dart()
        elif self.state == 'UPDATE_GAME':
            self.update_game()
        elif self.state == 'FINISH_GAME':
            self.finish_game()

    def select_game(self):
        print(self.state)
        option = input('Select Game: (1 - 501, 2 - Around the World) ')
        if option == '1':
            self.game = Game501()
        elif option == '2':
            self.game = GameAroundTheWorld()
        # Set transition
        self.action = 'game_selected'

    def idle_turn(self):
        print(self.state)
        os.system('pause')
        # Set transition
        self.action = 'profile_selected'

    def new_dart(self):
        print(self.state)
        self.client.send(constants.LOOK_MSG.encode())
        # Set transition
        self.action = 'look_msg_txd'

    def wait_dart(self):
        print(self.state)
        data = self.client.recv(constants.BUFFER_SIZE)
        constants.MSG = pickle.loads(data)
        self.number = constants.MSG["number"]
        self.ring = constants.MSG["ring"]
        # Set transition
        self.action = 'location_msg_rxd'

    def update_game(self):
        print(self.state)
        score = self.game.update(player=0, number=self.number, ring=self.ring)
        if self.game.get_winner(player=0):
            self.action = 'winner'
        else:
            self.action = 'no_winner'

    def finish_game(self):
        print(self.state)
        option = input('Play again? (y or n)')
        if option == 'Y' or option == 'y':
            self.action = 'again'
        elif option == 'N' or option == 'n':
            self.action = 'not_again'

if __name__ == '__main__':
    try:
        state_machine = ScoringStateMachine()
        while True:
            state_machine.run_state()
            state_machine.transition(action=state_machine.get_action())

    except Exception as e:
        print(e)
# EOF
