#!/usr/bin/env python3
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
import socket
import pickle
from datetime import datetime

import constants

from database import Database
from player import Player
from game_501 import Game501
from game_around_the_world import GameAroundTheWorld

class ScoringStateMachine:
    def __init__(self) -> None:
        self.state = 'IDLE_START'
        self.transitions = {
            # Action               Current State      Next state
            'start_pressed'    : {'IDLE_START'     : 'START'},
            'create_profile'   : {'START'          : 'CREATE_PROFILE'},
            'play'             : {'START'          : 'WAIT_PLAY'},
            'profile_created'  : {'CREATE_PROFILE' : 'START'},
            'upload'           : {'CREATE_PROFILE' : 'UPLOAD_PROFILE'},
            'ready_msg_rxd'    : {'WAIT_PLAY'      : 'SELECT_GAME'},
            'game_selected'    : {'SELECT_GAME'    : 'SELECT_PLAYERS'},
            'players_selected' : {'SELECT_PLAYERS' : 'IDLE_TURN'},
            'profile_selected' : {'IDLE_TURN'      : 'NEW_DART'},
            'look_msg_txd'     : {'NEW_DART'       : 'WAIT_DART'},
            'location_msg_rxd' : {'WAIT_DART'      : 'UPDATE_GAME'},
            'winner'           : {'UPDATE_GAME'    : 'FINISH_GAME'},
            'no_winner'        : {'UPDATE_GAME'    : 'IDLE_TURN'},
            'again'            : {'FINISH_GAME'    : 'SELECT_GAME'},
            'not_again'        : {'FINISH_GAME'    : 'IDLE_START'}
        }
        self.players = []
        self.player_num = 0
        self.database = Database()

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (constants.IP_ADDRESS, constants.PORT)
        self.client.connect(server_address)

    def disconnect(self):
        self.client.close()

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
        else:
            pass

    def idle_start(self):
        print(self.state)
        input('Press start...')
        self.action = 'start_pressed'

    def start(self):
        print(self.state)
        self.database.connect('DARTS.db')
        option = int(input('Create profile (1) or play (2) '))
        if option == 1:
            self.action = 'create_profile'
        elif option == 2:
            self.action = 'play'
        else:
            pass

    def create_profile(self):
        print(self.state)
        name = input('Enter name: ')
        username = input('Enter username: ')
        player = (name, username)
        self.database.insert_player(player)
        self.action = 'profile_created'

    def wait_play(self):
        print(self.state)
        # Connect to imaging system
        self.connect()
        # Wait for ready message from imaging system
        data = self.client.recv(constants.BUFFER_SIZE).decode()
        if data == constants.READY_MSG:
            self.action = 'ready_msg_rxd'

    def select_game(self):
        print(self.state)
        # Select game
        option = int(input('Select Game: (1 - 501, 2 - Around the World) '))
        if option == 1:
            game_id = self.database.select_game("501")
            self.game = Game501()
        elif option == 2:
            game_id = self.database.select_game("Around the World")
            self.game = GameAroundTheWorld()
        else:
            pass
        self.game_id = game_id[0]
        self.action = 'game_selected'

    def select_players(self):
        print(self.state)
        # Select players
        self.num_players = int(input('Enter number of players: '))
        for i in range(self.num_players):
            option = int(input('Select players: (1 - Guest, 2 - Load Profile) '))
            if option == 1:
                self.players.append(Player())
            elif option == 2:
                username = input('Enter username: ')
                player = self.database.select_player(username)
                self.players.append(Player(id=player[0][0],
                                           name=player[0][1], username=player[0][2],
                                           num_games=player[0][3], num_wins=player[0][4]))
                self.players[i].inc_num_games()
            else:
                pass
            self.action = 'players_selected'

    def idle_turn(self):
        print(self.state)
        # Select profile
        self.player_num = int(input('Select player: '))
        self.action = 'profile_selected'

    def new_dart(self):
        print(self.state)
        # Send look message to imaging system
        self.client.send(constants.LOOK_MSG.encode())
        self.action = 'look_msg_txd'

    def wait_dart(self):
        print(self.state)
        # Wait for location message from imaging system
        data = self.client.recv(constants.BUFFER_SIZE)
        constants.MSG = pickle.loads(data)
        self.number = constants.MSG["number"]
        self.ring = constants.MSG["ring"]
        self.players[self.player_num].update_number(self.number)
        self.players[self.player_num].update_ring(self.ring)
        self.action = 'location_msg_rxd'

    def update_game(self):
        print(self.state)
        # Update game scores
        score = self.game.update(player=self.player_num, number=self.number, ring=self.ring)
        print(score)
        if self.game.get_winner(player=self.player_num) == True:
            self.players[self.player_num].inc_num_wins()
            self.action = 'winner'
        else:
            self.action = 'no_winner'

    def finish_game(self):
        print(self.state)
        time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        # Update records if not a guest
        for i in range(self.num_players):
            player_id = self.players[i].get_id()
            if player_id != 0:
                # Update number record table
                number_hits = self.players[i].get_number_hits()
                number_record = (time, player_id, self.game_id, *number_hits)
                self.database.insert_number_record(number_record)
                # Update ring record table
                ring_hits = self.players[i].get_ring_hits()
                ring_record = (time, player_id, self.game_id, *ring_hits)
                self.database.insert_ring_record(ring_record)
                # Update player table (games, wins, id)
                num_games = self.players[i].get_num_games()
                num_wins = self.players[i].get_num_wins()
                player = (num_games, num_wins, player_id)
                self.database.update_player(player)

        option = input('Play again? (y or n) ')
        if option == 'Y' or option == 'y':
            self.action = 'again'
        elif option == 'N' or option == 'n':
            self.client.send(constants.DONE_MSG.encode())
            self.client.close()
            self.database.disconnect()
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
