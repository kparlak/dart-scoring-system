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
sys.path.append('..')
import constants
import socket
import os
import pickle

from game_501 import Game501
from game_around_the_world import GameAroundTheWorld

class ScoringStateMachine:
    def __init__(self):
        self.state = 'IDLE_START'
        self.transitions = {
            # Action              Current State   Next state
            'start_pressed'    : {'IDLE_START'     : 'START'},
            'create_profile'   : {'START'          : 'CREATE_PROFILE'},
            'play'             : {'START'          : 'WAIT_PLAY'},
            'profile_created'  : {'CREATE_PROFILE' : 'START'},
            'upload'           : {'CREATE_PROFILE' : 'UPLOAD_PROFILE'},
            'ready_msg_rxd'    : {'WAIT_PLAY'      : 'SELECT_GAME'},
            'game_selected'    : {'SELECT_GAME'    : 'IDLE_TURN'},
            'profile_selected' : {'IDLE_TURN'      : 'NEW_DART'},
            'look_msg_txd'     : {'NEW_DART'       : 'WAIT_DART'},
            'location_msg_rxd' : {'WAIT_DART'      : 'UPDATE_GAME'},
            'winner'           : {'UPDATE_GAME'    : 'FINISH_GAME'},
            'no_winner'        : {'UPDATE_GAME'    : 'IDLE_TURN'},
            'again'            : {'FINISH_GAME'    : 'SELECT_GAME'},
            'not_again'        : {'FINISH_GAME'    : 'IDLE_START'}
        }
        self.num_players = 0

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (constants.IP_ADDRESS, constants.PORT)
        self.client.connect(server_address)

    def get_action(self):
        return self.action

    def transition(self, action):
        if action in self.transitions.keys():
            self.state = self.transitions[action][self.state]

    def run_state(self):
        if self.state == 'IDLE_START':
            self.idle_start()
        elif self.state == 'START':
            self.start()
        elif self.state == 'CREATE_PROFILE':
            self.create_profile()
        elif self.state == 'WAIT_PLAY':
            self.wait_play()
        elif self.state == 'SELECT_GAME':
            self.select_game()
        elif self.state == 'SELECT_PLAYERS':
            self.select_players()
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

    def idle_start(self):
        print(self.state)
        os.system('pause')
        self.action = 'start_pressed'

    def start(self):
        print(self.state)
        self.action = 'play'

    def create_profile(self):
        print(self.state)
        self.action = 'start_pressed'

    def wait_play(self):
        print(self.state)
        self.connect()
        data = self.client.recv(constants.BUFFER_SIZE).decode()
        if (data == constants.READY_MSG):
            self.action = 'ready_msg_rxd'

    def select_game(self):
        print(self.state)
        option = input('Select Game: (1 - 501, 2 - Around the World) ')
        if option == 1:
            self.game = Game501()
        elif option == 2:
            self.game = GameAroundTheWorld()
        self.action = 'game_selected'

    def select_players(self):
        print(self.state)
        self.action = 'players_selected'

    def idle_turn(self):
        print(self.state)
        os.system('pause')
        self.action = 'profile_selected'

    def new_dart(self):
        print(self.state)
        self.client.send(constants.LOOK_MSG.encode())
        self.action = 'look_msg_txd'

    def wait_dart(self):
        print(self.state)
        data = self.client.recv(constants.BUFFER_SIZE)
        constants.MSG = pickle.loads(data)
        self.number = constants.MSG["number"]
        self.ring = constants.MSG["ring"]
        self.action = 'location_msg_rxd'

    def update_game(self):
        print(self.state)
        score = self.game.update(player=0, number=self.number, ring=self.ring)
        print(score)
        if self.game.get_winner(player=0) == True:
            self.action = 'winner'
        else:
            self.action = 'no_winner'

    def finish_game(self):
        print(self.state)
        option = input('Play again? (y or n) ')
        if option == 'Y' or option == 'y':
            self.action = 'again'
        elif option == 'N' or option == 'n':
            self.client.send(constants.DONE_MSG.encode())
            self.client.close()
            self.action = 'not_again'

if __name__ == '__main__':
    try:
        sm = ScoringStateMachine()
        while True:
            sm.run_state()
            sm.transition(action=sm.get_action())

    except Exception as e:
        print(e)

# EOF
