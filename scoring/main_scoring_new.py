#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   ui.py
@Time    :   2023/11/16
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Main for scoring system
'''

import sys
sys.path.append('..')
import socket

import constants

from PyQt5.QtWidgets import QApplication, QMainWindow

from ui.idle_start_display import Ui_IdleStartDisplay
from ui.start_display import Ui_StartDisplay
from ui.create_profile_display import Ui_CreateProfileDisplay
from ui.select_game_display import Ui_SelectGameDisplay
from ui.select_players_display import Ui_SelectPlayersDisplay

from database import Database
from player import Player
from game_501 import Game501
from game_around_the_world import GameAroundTheWorld

database = Database()
database.connect('DARTS.db')
# TODO : Adjust state machine diagram for scoring system

# Globals
game = None
players = []
num_players = 0
max_players = 0

class IdleStartDisplay(QMainWindow, Ui_IdleStartDisplay):
    def __init__(self, parent=None):
        super(IdleStartDisplay, self).__init__(parent)
        self.setupUi(self)
        self.startButton.clicked.connect(self.start_button)

    def start_button(self):
        self.close()

class StartDisplay(QMainWindow, Ui_StartDisplay):
    def __init__(self, parent=None):
        super(StartDisplay, self).__init__(parent)
        self.setupUi(self)
        self.createProfileButton.clicked.connect(self.create_profile_button)
        self.selectGameButton.clicked.connect(self.select_game_button)
        self.cancelButton.clicked.connect(self.close)

    def create_profile_button(self):
        self.close()

    def select_game_button(self):
        # TODO : Connect to imaging system
        self.close()

class CreateProfileDisplay(QMainWindow, Ui_CreateProfileDisplay):
    def __init__(self, parent=None):
        super(CreateProfileDisplay, self).__init__(parent)
        self.setupUi(self)
        self.uploadButton.clicked.connect(self.upload_button)
        self.cancelButton.clicked.connect(self.close)

    def upload_button(self):
        name = self.nameInput.toPlainText()
        username = self.usernameInput.toPlainText()
        database.insert_player((name, username))
        self.close()

class SelectGameDisplay(QMainWindow, Ui_SelectGameDisplay):
    def __init__(self, parent=None):
        super(SelectGameDisplay, self).__init__(parent)
        self.setupUi(self)
        self.selectPlayersButton.clicked.connect(self.select_players_button)
        self.cancelButton.clicked.connect(self.cancel_button)

    def select_players_button(self):
        if self.gameBox.currentText() == '501':
            game = Game501()
        elif self.gameBox.currentText() == 'Around the World':
            game = GameAroundTheWorld()
        global max_players
        max_players = game.get_num_players()
        self.close()

    def cancel_button(self):
        game = None
        self.close()

class SelectPlayersDisplay(QMainWindow, Ui_SelectPlayersDisplay):
    def __init__(self, parent=None):
        super(SelectPlayersDisplay, self).__init__(parent)
        self.setupUi(self)
        self.loadButton.clicked.connect(self.load_button)
        self.guestButton.clicked.connect(self.guest_button)
        self.cancelButton.clicked.connect(self.cancel_button)

    def load_button(self):
        global num_players
        if num_players == max_players:
            self.loadButton.setEnabled(False)
        username = self.usernameInput.toPlainText()
        player = database.select_player(username)
        players.append(Player(id=player[0][0],
                              name=player[0][1], username=player[0][2],
                              num_games=player[0][3], num_wins=player[0][4]))
        output = 'Player ' + str(num_players) + ': ' + players[num_players - 1].get_username() +'\n'
        self.playersOutput.insertPlainText(output)

    def guest_button(self):
        global num_players
        if num_players > max_players:
            self.guestButton.setEnabled(False)
        players.append(Player())
        num_players += 1
        output = 'Player ' + str(num_players) + ': ' + players[num_players - 1].get_username() + '\n'
        self.playersOutput.insertPlainText(output)

    def cancel_button(self):
        global num_players
        num_players = 0
        players = []
        self.playersOutput.clear()
        self.close()

class UserInterface():
    def __init__(self):
        self.first = IdleStartDisplay()
        self.second = StartDisplay()
        self.third = CreateProfileDisplay()
        self.fourth = SelectGameDisplay()
        self.fifth = SelectPlayersDisplay()

        # Transitions
        # self.first.helpButton.clicked.connect()
        self.first.startButton.clicked.connect(self.second.show)

        # self.second.helpButton.clicked.connect()
        self.second.createProfileButton.clicked.connect(self.third.show)
        self.second.selectGameButton.clicked.connect(self.fourth.show)
        self.second.cancelButton.clicked.connect(self.first.show)

        # self.third.helpButton.clicked.connect()
        self.third.uploadButton.clicked.connect(self.second.show)
        self.third.cancelButton.clicked.connect(self.second.show)

        # self.fourth.helpButton.clicked.connect()
        self.fourth.selectPlayersButton.clicked.connect(self.fifth.show)
        self.fourth.cancelButton.clicked.connect(self.second.show)

        # self.fifth.helpButton.clicked.connect()
        self.fifth.cancelButton.clicked.connect(self.fourth.show)

        self.first.show()


# TODO : Make a class
def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (constants.IP_ADDRESS, constants.PORT)
    client.connect(server_address)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UserInterface()
    sys.exit(app.exec())

# EOF
