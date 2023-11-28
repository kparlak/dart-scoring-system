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
import pickle
import time

import constants

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QMovie

from ui.idle_start_display import Ui_IdleStartDisplay
from ui.start_display import Ui_StartDisplay
from ui.create_profile_display import Ui_CreateProfileDisplay
from ui.select_game_display import Ui_SelectGameDisplay
from ui.select_players_display import Ui_SelectPlayersDisplay
from ui.scoreboard_display import Ui_ScoreboardDisplay

from database import Database
from player import Player
from game_501 import Game501
from game_around_the_world import GameAroundTheWorld

database = Database('/data/DARTS.db')

# Globals
game = None
players = []
client = None
num_players = 0

class Icon(QIcon):
    def __init__(self, parent=None):
        super(Icon, self).__init__(parent)
        self.addPixmap(QPixmap("ui/DARTS_Icon.png"), QIcon.Normal, QIcon.Off)

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
        self.icon = Icon()
        self.setWindowIcon(self.icon)
        self.movie = QMovie("ui/DARTS_Startup_Resized.gif")
        self.movieLabel.setMovie(self.movie)
        self.movie.start()
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
        self.icon = Icon()
        self.setWindowIcon(self.icon)
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
        self.icon = Icon()
        self.setWindowIcon(self.icon)
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
        self.icon = Icon()
        self.setWindowIcon(self.icon)
        self.helpBox = HelpBox()
        self.helpButton.clicked.connect(self.help_button)
        self.selectPlayersButton.clicked.connect(self.select_players_button)
        self.cancelButton.clicked.connect(self.cancel_button)

    def help_button(self):
        self.helpBox.setText('TODO')
        self.helpBox.exec()

    def select_players_button(self):
        global game
        if self.gameBox.currentText() == '501':
            game = Game501()
        elif self.gameBox.currentText() == 'Around the World':
            game = GameAroundTheWorld()
        self.close()

    def cancel_button(self):
        game = None
        self.close()

class SelectPlayersDisplay(QMainWindow, Ui_SelectPlayersDisplay):
    def __init__(self, parent=None):
        super(SelectPlayersDisplay, self).__init__(parent)
        self.setupUi(self)
        self.icon = Icon()
        self.setWindowIcon(self.icon)
        self.helpBox = HelpBox()
        self.errorBox = ErrorBox()
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
        username = self.usernameInput.toPlainText()
        player = database.select_player(username)
        # Load profile if valid username
        if len(player) == 0:
            self.errorBox.setText('Bad username')
            self.errorBox.exec()
        else:
            players.append(Player(id=player[0][0],
                                  name=player[0][1], username=player[0][2],
                                  num_games=player[0][3], num_wins=player[0][4]))
            num_players += 1
            output = 'Player ' + str(num_players) + ': ' + players[num_players - 1].get_username() +'\n'
            self.playersOutput.insertPlainText(output)
            self.usernameInput.clear()
            self.playButton.setEnabled(True)
            # Disable buttons if max number of players
            if num_players == game.get_num_players():
                self.loadButton.setEnabled(False)
                self.guestButton.setEnabled(False)

    def guest_button(self):
        global num_players
        players.append(Player())
        num_players += 1
        output = 'Player ' + str(num_players) + ': ' + players[num_players - 1].get_username() + '\n'
        self.playersOutput.insertPlainText(output)
        self.playButton.setEnabled(True)
        # Disable buttons if max number of players
        if num_players == game.get_num_players():
            self.guestButton.setEnabled(False)
            self.loadButton.setEnabled(False)

    def play_button(self):
        self.close()
        # TODO : Connect to imaging system

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

class ScoreboardDisplay(QMainWindow, Ui_ScoreboardDisplay):
    def __init__(self, parent=None):
        super(ScoreboardDisplay, self).__init__(parent)
        self.setupUi(self)
        self.icon = Icon()
        self.setWindowIcon(self.icon)
        self.helpBox = HelpBox()
        self.player1Button.setEnabled(True)
        self.player2Button.setEnabled(False)
        self.helpButton.clicked.connect(self.help_button)
        self.player1Button.clicked.connect(self.player1_button)
        self.player2Button.clicked.connect(self.player2_button)
        self.quitButton.clicked.connect(self.quit_button)
        self.num_turns = 0

    def help_button(self):
        self.helpBox.setText('TODO')
        self.helpBox.exec()

    def player1_button(self):
        self.num_turns += 1
        # Send look message
        client.send(constants.LOOK_MSG.encode())
        # Wait on location message
        # self.player1Button.setEnabled(False)
        data = client.recv(constants.BUFFER_SIZE)
        # Deserialize data from socket
        constants.MSG = pickle.loads(data)
        number = constants.MSG["number"]
        ring = constants.MSG["ring"]
        # Update score
        score = game.update(player=0, number=number, ring=ring)
        self.player1Score.display(score)
        # Update player statistics
        players[0].inc_num_throws()
        players[0].update_number(number)
        players[0].update_ring(ring)
        # Switch player
        if len(players) > 1 and self.num_turns == game.get_num_turns():
            self.num_turns = 0
            self.player1Button.setEnabled(False)
            self.player2Button.setEnabled(True)

    def player2_button(self):
        self.num_turns += 1
        # Send look message
        client.send(constants.LOOK_MSG.encode())
        # Wait on location message
        data = client.recv(constants.BUFFER_SIZE)
        # Deserialize data from socket
        constants.MSG = pickle.loads(data)
        number = constants.MSG["number"]
        ring = constants.MSG["ring"]
        # Update score
        score = game.update(player=1, number=number, ring=ring)
        self.player2Score.display(score)
        # Update player statistics
        players[1].inc_num_throws()
        players[1].update_number(number)
        players[1].update_ring(ring)
        # Switch player
        if self.num_turns == game.get_num_turns():
            self.num_turns = 0
            self.player2Button.setEnabled(False)
            self.player1Button.setEnabled(True)

    def quit_button(self):
        pass
        # self.close()

    def update_game(self):
        pass

class UserInterface():
    def __init__(self):
        self.first = IdleStartDisplay()
        self.second = StartDisplay()
        self.third = CreateProfileDisplay()
        self.fourth = SelectGameDisplay()
        self.fifth = SelectPlayersDisplay()
        self.sixth = ScoreboardDisplay()

        # Transitions
        self.first.startButton.clicked.connect(self.second.show)

        self.second.createProfileButton.clicked.connect(self.third.show)
        self.second.selectGameButton.clicked.connect(self.fourth.show)
        self.second.cancelButton.clicked.connect(self.first.show)

        self.third.uploadButton.clicked.connect(self.second.show)
        self.third.cancelButton.clicked.connect(self.second.show)

        self.fourth.selectPlayersButton.clicked.connect(self.fifth.show)
        self.fourth.cancelButton.clicked.connect(self.second.show)

        self.fifth.playButton.clicked.connect(self.play_button)
        self.fifth.cancelButton.clicked.connect(self.fourth.show)

        # self.sixth.quitButton.clicked.connect(self.second.show)

        self.first.show()

    def play_button(self):
        # Connect to imaging system
        connect()
        # Wait for READY message
        msg_box = QMessageBox(text='Waiting to connect...')
        msg_box.exec()
        # TODO : pop-up dialog indicating system is waiting
        data = client.recv(constants.BUFFER_SIZE).decode()
        if data == constants.READY_MSG:
            self.sixth.show()
            self.sixth.setWindowTitle(game.get_name())
            # Load players
            for i in range(len(players)):
                if i == 0:
                    self.sixth.player1UsernameOutput.insertPlainText(players[0].get_username())
                    self.sixth.player1Score.display(game.get_score(player=0))
                elif i == 1:
                    self.sixth.player2UsernameOutput.insertPlainText(players[1].get_username())
                    self.sixth.player2Score.display(game.get_score(player=1))
                else:
                    pass

def connect():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (constants.IP_ADDRESS, constants.PORT)
    client.connect(server_address)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UserInterface()
    sys.exit(app.exec())

# EOF
