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
    def __init__(self):
        self.state = 'IDLE_START'
        self.transitions = {
            # Action               Current State      Next state
            'start'            : {'IDLE_START'     : 'START'},
            'create_profile'   : {'START'          : 'CREATE_PROFILE'},
            'select_game'      : {'START'          : 'SELECT_GAME'},
            'cancel_start'     : {'START'          : 'IDLE_START'},
            'upload_profile'   : {'CREATE_PROFILE' : 'START'},
            'cancel_profile'   : {'CREATE_PROFILE' : 'START'},
            'game_selected'    : {'SELECT_GAME'    : 'SELECT_PLAYERS'},
            'cancel_game'      : {'SELECT_GAME'    : 'START'},
            'players_selected' : {'SELECT_PLAYERS' : 'WAIT_PLAY'},
            'cancel_players'   : {'SELECT_PLAYERS' : 'SELECT_GAME'},
            'ready_msg_rxd'    : {'WAIT_PLAY'      : 'IDLE_TURN'},
            'player_selected'  : {'IDLE_TURN'      : 'NEW_DART'},
            'play_quit'        : {'IDLE_TURN'      : 'FINISH_GAME'},
            'look_msg_txd'     : {'NEW_DART'       : 'WAIT_DART'},
            'location_msg_rxd' : {'WAIT_DART'      : 'UPDATE_GAME'},
            'winner'           : {'UPDATE_GAME'    : 'FINISH_GAME'},
            'no_winner'        : {'UPDATE_GAME'    : 'IDLE_TURN'},
            'again'            : {'FINISH_GAME'    : 'WAIT_PLAY'},
            'not_again'        : {'FINISH_GAME'    : 'IDLE_START'}
        }
        self.players = []
        self.turn_num = 0
        self.player_num = 0
        self.database = Database('DARTS.db')

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
        elif self.state == 'SELECT_GAME':
            self.select_game()
        elif self.state == 'SELECT_PLAYERS':
            self.select_players()
        elif self.state == 'WAIT_PLAY':
            self.wait_play()
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
        input('Press enter to start...')
        self.action = 'start'

    def start(self):
        print(self.state)
        option = int(input('Create Profile (1), Select Game (2), Cancel (3) '))
        if option == 1:
            self.action = 'create_profile'
        elif option == 2:
            self.action = 'select_game'
        elif option == 3:
            self.action = 'cancel_start'
        else:
            pass

    def create_profile(self):
        print(self.state)
        name = input('Name: ')
        username = input('Username: ')
        player = (name, username)
        option = int(input('Upload (1), Cancel (2) '))
        if option == 1:
            self.database.insert_player(player)
            self.action = 'upload_profile'
        elif option == 2:
            self.action = 'cancel_profile'
        else:
            pass

    def select_game(self):
        print(self.state)
        option = int(input('501 (1), Around the World (2), Cancel (3) '))
        if option == 1:
            game_id = self.database.select_game('501')
            self.game_id = game_id[0]
            self.game = Game501()
            self.action = 'game_selected'
        elif option == 2:
            game_id = self.database.select_game('Around the World')
            self.game_id = game_id[0]
            self.game = GameAroundTheWorld()
            self.action = 'game_selected'
        elif option == 3:
            self.game_id = None
            self.game = None
            self.action = 'cancel_game'
        else:
            pass

    def select_players(self):
        print(self.state)
        # Load guests or player profiles
        for i in range(self.game.get_num_players()):
            option = int(input('Guest (1), Load Profile (2), Play (3), Cancel (4) '))
            if option == 1:
                self.players.append(Player())
                self.action = 'players_selected'
            elif option == 2:
                username = input('Username: ')
                player = self.database.select_player(username)
                self.players.append(Player(id=player[0][0],
                            name=player[0][1], username=player[0][2],
                            num_throws=player[0][3], num_games=player[0][4],
                            num_wins=player[0][5]))
                self.action = 'players_selected'
            elif option == 3:
                self.action = 'players_selected'
                break
            elif option == 4:
                self.players[:] = []
                self.action = 'cancel_players'
                break
            else:
                pass

    def wait_play(self):
        print(self.state)
        # Increment game count for player profile
        for i in range(len(self.players)):
            self.players[i].inc_num_games()
        # Connect to imaging system
        self.connect()
        # Wait for ready message from imaging system
        data = self.client.recv(constants.BUFFER_SIZE).decode()
        if data == constants.READY_MSG:
            self.action = 'ready_msg_rxd'

    def idle_turn(self):
        print(self.state)
        # Take turns based on game
        if len(self.players) > 1:
            # Switch players if number of turns
            if self.turn_num == self.game.get_num_turns():
                self.turn_num = 0
                self.player_num += 1
            # Reset if max players
            if self.player_num == len(self.players):
                self.player_num = 0
            print('Player ' + str(self.player_num + 1))
        else:
            print('Player 1')
            self.player_num = 0
        option = int(input('Throw (0), Quit (1) '))
        if option == 0:
            self.turn_num += 1
            self.action = 'player_selected'
        elif option == 1:
            self.action = 'play_quit'
        else:
            pass

    def new_dart(self):
        print(self.state)
        # Send look message to imaging system
        self.client.send(constants.LOOK_MSG.encode())
        self.action = 'look_msg_txd'

    def wait_dart(self):
        print(self.state)
        # Wait for location message from imaging system
        data = self.client.recv(constants.BUFFER_SIZE)
        # Deserialize data from socket
        constants.MSG = pickle.loads(data)
        self.number = constants.MSG["number"]
        self.ring = constants.MSG["ring"]
        # Update player statistics
        self.players[self.player_num].inc_num_throws()
        self.players[self.player_num].update_number(self.number)
        self.players[self.player_num].update_ring(self.ring)
        self.action = 'location_msg_rxd'

    def update_game(self):
        print(self.state)
        # Update game scores
        score = self.game.update(player=self.player_num, number=self.number, ring=self.ring)
        print(score)
        # Check for a winner
        if self.game.get_winner(player=self.player_num) == True:
            self.players[self.player_num].inc_num_wins()
            self.action = 'winner'
        else:
            self.action = 'no_winner'

    def finish_game(self):
        print(self.state)
        time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        # Update records if not a guest
        for i in range(len(self.players)):
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
                # Update player table (throws, games, wins, id)
                num_throws = self.players[i].get_num_throws()
                num_games = self.players[i].get_num_games()
                num_wins = self.players[i].get_num_wins()
                player = (num_throws, num_games, num_wins, player_id)
                self.database.update_player(player)
        # Disconnect
        self.client.send(constants.DONE_MSG.encode())
        self.client.close()
        # Reset counters
        self.turn_num = 0
        self.player_num = 0
        option = input('Play again? (y or n) ')
        if option == 'Y' or option == 'y':
            self.game.reset()
            for i in range(len(self.players)):
                self.players[i].reset()
            self.action = 'again'
        elif option == 'N' or option == 'n':
            self.players[:] = []
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
