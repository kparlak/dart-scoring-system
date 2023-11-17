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

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

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

class HelpBox(QMessageBox):
    def __init__(self, parent=None):
        super(HelpBox, self).__init__(parent)
        self.setWindowTitle('Help')

class ErrorBox(QMessageBox):
    def __init__(self, parent=None):
        super(ErrorBox, self).__init__(parent)
        self.setWindowTitle('Error')

class IdleStartDisplay(QMainWindow, Ui_IdleStartDisplay):
    def __init__(self, parent=None):
        super(IdleStartDisplay, self).__init__(parent)
        self.setupUi(self)
        self.helpBox = HelpBox()
        self.helpButton.clicked.connect(self.help_button)
        self.startButton.clicked.connect(self.start_button)

    def help_button(self):
        self.helpBox.setText('Press Start to Begin')
        self.helpBox.exec()

    def start_button(self):
        self.close()

class StartDisplay(QMainWindow, Ui_StartDisplay):
    def __init__(self, parent=None):
        super(StartDisplay, self).__init__(parent)
        self.setupUi(self)
        self.helpBox = HelpBox()
        self.helpButton.clicked.connect(self.help_button)
        self.createProfileButton.clicked.connect(self.create_profile_button)
        self.selectGameButton.clicked.connect(self.select_game_button)
        self.cancelButton.clicked.connect(self.close)

    def help_button(self):
        self.helpBox.setText('TODO')
        self.helpBox.exec()

    def create_profile_button(self):
        self.close()

    def select_game_button(self):
        self.close()

class CreateProfileDisplay(QMainWindow, Ui_CreateProfileDisplay):
    def __init__(self, parent=None):
        super(CreateProfileDisplay, self).__init__(parent)
        self.setupUi(self)
        self.helpBox = HelpBox()
        self.helpButton.clicked.connect(self.help_button)
        self.uploadButton.clicked.connect(self.upload_button)
        self.cancelButton.clicked.connect(self.close)

    def help_button(self):
        self.helpBox.setText('TODO')
        self.helpBox.exec()

    def upload_button(self):
        name = self.nameInput.toPlainText()
        username = self.usernameInput.toPlainText()
        database.insert_player((name, username))
        self.close()

class SelectGameDisplay(QMainWindow, Ui_SelectGameDisplay):
    def __init__(self, parent=None):
        super(SelectGameDisplay, self).__init__(parent)
        self.setupUi(self)
        self.helpBox = HelpBox()
        self.helpButton.clicked.connect(self.help_button)
        self.selectPlayersButton.clicked.connect(self.select_players_button)
        self.cancelButton.clicked.connect(self.cancel_button)

    def help_button(self):
        self.helpBox.setText('TODO')
        self.helpBox.exec()

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
        self.helpBox = HelpBox()
        self.errorBox = ErrorBox()
        self.setupUi(self)
        self.playButton.setEnabled(False)
        self.helpButton.clicked.connect(self.help_button)
        self.loadButton.clicked.connect(self.load_button)
        self.guestButton.clicked.connect(self.guest_button)
        self.playButton.clicked.connect(self.play_button)
        self.cancelButton.clicked.connect(self.cancel_button)

    def help_button(self):
        self.helpBox.setText('TODO')
        self.helpBox.exec()

    def load_button(self):
        global num_players
        if num_players == max_players - 1:
            self.loadButton.setEnabled(False)
            self.guestButton.setEnabled(False)
        username = self.usernameInput.toPlainText()
        player = database.select_player(username)
        if len(player) == 0:
            self.errorBox.setText('Bad username')
            self.errorBox.exec()
        else:
            players.append(Player(id=player[0][0],
                                  name=player[0][1], username=player[0][2],
                                  num_games=player[0][3], num_wins=player[0][4]))
            num_players += 1
            output = 'Player ' + str(num_players) + ': ' + players[num_players - 1].get_username() +'\n'
            print(players[num_players - 1].get_username())
            self.playersOutput.insertPlainText(output)
            self.usernameInput.clear()

    def guest_button(self):
        global num_players
        if num_players == max_players - 1:
            self.guestButton.setEnabled(False)
            self.loadButton.setEnabled(False)
        players.append(Player())
        num_players += 1
        output = 'Player ' + str(num_players) + ': ' + players[num_players - 1].get_username() + '\n'
        self.playersOutput.insertPlainText(output)

    def play_button(self):
        # TODO : Connect to imaging system
        pass

    def cancel_button(self):
        global num_players
        num_players = 0
        players[:] = []
        self.playersOutput.clear()
        self.usernameInput.clear()
        self.loadButton.setEnabled(True)
        self.guestButton.setEnabled(True)
        self.playButton.setEnabled(False)
        self.close()

class UserInterface():
    def __init__(self):
        self.first = IdleStartDisplay()
        self.second = StartDisplay()
        self.third = CreateProfileDisplay()
        self.fourth = SelectGameDisplay()
        self.fifth = SelectPlayersDisplay()

        # Transitions
        self.first.startButton.clicked.connect(self.second.show)

        self.second.createProfileButton.clicked.connect(self.third.show)
        self.second.selectGameButton.clicked.connect(self.fourth.show)
        self.second.cancelButton.clicked.connect(self.first.show)

        self.third.uploadButton.clicked.connect(self.second.show)
        self.third.cancelButton.clicked.connect(self.second.show)

        self.fourth.selectPlayersButton.clicked.connect(self.fifth.show)
        self.fourth.cancelButton.clicked.connect(self.second.show)

        # self.fifth.playButton.clicked.connect(self.sixth.show)
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
