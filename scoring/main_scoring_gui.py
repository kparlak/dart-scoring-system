#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   main_scoring_gui.py
@Time    :   2023/11/28
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Main for scoring system GUI
'''

import sys
sys.path.append('..')
import socket
import pickle
from datetime import datetime

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

# Globals
database = Database('DARTS.db')
game = None
players = []
client = None

class Icon(QIcon):
    def __init__(self, parent=None):
        super(Icon, self).__init__(parent)
        self.addPixmap(QPixmap("ui/DARTS_Icon.png"), QIcon.Normal, QIcon.Off)

class IdleStartDisplay(QMainWindow, Ui_IdleStartDisplay): # DONE
    def __init__(self, parent=None):
        super(IdleStartDisplay, self).__init__(parent)
        self.setupUi(self)
        self.icon = Icon()
        self.setWindowIcon(self.icon)
        self.movie = QMovie("ui/DARTS_Startup_Resized.gif")
        self.movieLabel.setMovie(self.movie)
        self.movie.start()
        self.helpButton.clicked.connect(self.help_button)
        self.startButton.clicked.connect(self.close)

    def help_button(self):
        QMessageBox.information(self, 'Help',
                                'Press Start to begin')

class StartDisplay(QMainWindow, Ui_StartDisplay): # DONE
    def __init__(self, parent=None):
        super(StartDisplay, self).__init__(parent)
        self.setupUi(self)
        self.icon = Icon()
        self.setWindowIcon(self.icon)
        self.helpButton.clicked.connect(self.help_button)
        self.createProfileButton.clicked.connect(self.close)
        self.selectGameButton.clicked.connect(self.close)
        self.cancelButton.clicked.connect(self.close)

    def help_button(self):
        QMessageBox.information(self, 'Help',
                                'Create a player profile or select a game to play')

class CreateProfileDisplay(QMainWindow, Ui_CreateProfileDisplay): # DONE
    def __init__(self, parent=None):
        super(CreateProfileDisplay, self).__init__(parent)
        self.setupUi(self)
        self.icon = Icon()
        self.setWindowIcon(self.icon)
        self.helpButton.clicked.connect(self.help_button)
        self.cancelButton.clicked.connect(self.cancel_button)

    def help_button(self):
        QMessageBox.information(self, 'Help',
                                'Enter name and username and upload to database')

    def cancel_button(self):
        self.nameInput.clear()
        self.usernameInput.clear()
        self.close()

class SelectGameDisplay(QMainWindow, Ui_SelectGameDisplay): # DONE
    def __init__(self, parent=None):
        super(SelectGameDisplay, self).__init__(parent)
        self.setupUi(self)
        self.icon = Icon()
        self.setWindowIcon(self.icon)
        self.helpButton.clicked.connect(self.help_button)
        self.cancelButton.clicked.connect(self.close)

    def help_button(self):
        QMessageBox.information(self, 'Help',
                                'Select game from dropdown')

class SelectPlayersDisplay(QMainWindow, Ui_SelectPlayersDisplay): # DONE
    def __init__(self, parent=None):
        super(SelectPlayersDisplay, self).__init__(parent)
        self.setupUi(self)
        self.icon = Icon()
        self.setWindowIcon(self.icon)
        self.playButton.setEnabled(False)
        self.helpButton.clicked.connect(self.help_button)
        self.playButton.clicked.connect(self.reset)
        self.cancelButton.clicked.connect(self.cancel_button)

    def reset(self):
        self.playersOutput.clear()
        self.usernameInput.clear()
        self.loadButton.setEnabled(True)
        self.guestButton.setEnabled(True)
        self.playButton.setEnabled(False)

    def help_button(self):
        QMessageBox.information(self, 'Help',
                                'TODO')

    def cancel_button(self):
        players[:] = []
        self.reset()
        self.close()

class ScoreboardDisplay(QMainWindow, Ui_ScoreboardDisplay):
    def __init__(self, parent=None):
        super(ScoreboardDisplay, self).__init__(parent)
        self.setupUi(self)
        self.icon = Icon()
        self.setWindowIcon(self.icon)
        self.player1Button.setEnabled(True)
        self.player2Button.setEnabled(False)
        self.helpButton.clicked.connect(self.help_button)

    def reset_buttons(self):
        self.player1Button.setEnabled(True)
        self.player2Button.setEnabled(False)

    def reset_text(self):
        self.player1UsernameOutput.clear()
        self.player2UsernameOutput.clear()

    def help_button(self):
        QMessageBox.information(self, 'Help',
                                'Select player prior to throwing')

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

        self.third.uploadButton.clicked.connect(self.upload_button)
        self.third.cancelButton.clicked.connect(self.second.show)

        self.fourth.selectPlayersButton.clicked.connect(self.select_players_button)
        self.fourth.cancelButton.clicked.connect(self.second.show)

        self.fifth.loadButton.clicked.connect(self.load_button)
        self.fifth.guestButton.clicked.connect(self.guest_button)
        self.fifth.playButton.clicked.connect(self.play_button)
        self.fifth.cancelButton.clicked.connect(self.fourth.show)

        self.sixth.player1Button.clicked.connect(self.player1_button)
        self.sixth.player2Button.clicked.connect(self.player2_button)
        self.sixth.quitButton.clicked.connect(self.quit_button)

        self.first.show()

        self.num_turns = 0

    def upload_button(self):
        name = self.third.nameInput.toPlainText()
        username = self.third.usernameInput.toPlainText()
        if name == '' and username == '':
            QMessageBox.critical(self.third, 'Upload Error',
                                 'Name and username are blank')
        else:
            database.insert_player((name, username))
            QMessageBox.information(self.third, 'Upload', # TODO : Better vergabe
                                    'Upload Successful')
            self.third.close()
            self.second.show()
        self.third.nameInput.clear()
        self.third.usernameInput.clear()

    def select_players_button(self):
        global game
        if self.fourth.gameBox.currentText() == '501':
            game = Game501()
        elif self.fourth.gameBox.currentText() == 'Around the World':
            game = GameAroundTheWorld()
        else:
            pass
        self.fourth.close()
        self.fifth.show()

    def load_button(self):
        username = self.fifth.usernameInput.toPlainText()
        player = database.select_player(username)
        # Load profile if valid username
        if username == '' or len(player) == 0:
            QMessageBox.critical(self.fifth, 'Help', # TODO : Better title
                                 'Username not valid')
            self.fifth.usernameInput.clear()
        else:
            players.append(Player(id=player[0][0],
                                  name=player[0][1], username=player[0][2],
                                  num_throws=player[0][3], num_games=player[0][4], num_wins=player[0][5]))
            output = 'Player ' + str(len(players)) + ': ' + players[len(players) - 1].get_username() + '\n'
            self.fifth.playersOutput.insertPlainText(output)
            self.fifth.usernameInput.clear()
            self.fifth.playButton.setEnabled(True)
            # Disable buttons if max number of players
            if len(players) == game.get_num_players():
                self.fifth.loadButton.setEnabled(False)
                self.fifth.guestButton.setEnabled(False)

    def guest_button(self):
        players.append(Player())
        output = 'Player ' + str(len(players)) + ': ' + players[len(players) - 1].get_username() + '\n'
        self.fifth.playersOutput.insertPlainText(output)
        self.fifth.playButton.setEnabled(True)
        # Disable buttons if max number of players
        if len(players) == game.get_num_players():
            self.fifth.guestButton.setEnabled(False)
            self.fifth.loadButton.setEnabled(False)

    def play_button(self):
        for i in range(len(players)):
            players[i].inc_num_games()
        # Connect to imaging system
        connect()
        # Wait for READY message
        self.fifth.close()
        QMessageBox.information(self.fifth, 'dd', # TODO : Label correctly
                                'Connecting to imaging system...')
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

    def player_button(self, player):
        self.num_turns += 1
        # Send look message
        client.send(constants.LOOK_MSG.encode())
        # Disable button to wait for event
        if player == 0:
            self.sixth.player1Button.setEnabled(False)
        elif player == 1:
            self.sixth.player2Button.setEnabled(False)
        else:
            pass
        QApplication.processEvents()
        # Wait on location message
        data = client.recv(constants.BUFFER_SIZE)
        # Deserialize data from socket
        constants.MSG = pickle.loads(data)
        number = constants.MSG["number"]
        ring = constants.MSG["ring"]
        # Update score
        score = game.update(player=player, number=number, ring=ring)
        if player == 0:
            self.sixth.player1Score.display(score)
        elif player == 1:
            self.sixth.player2Score.display(score)
        else:
            pass
        # Update player statistics
        players[player].inc_num_throws()
        players[player].update_number(number)
        players[player].update_ring(ring)
        # Check winner
        if game.get_winner(player=player) == True:
            players[player].inc_num_wins()
            update_records()
            reply = QMessageBox.question(self.sixth,
                                         'Player ' + str(player + 1) + ' wins!',
                                         'Play again?',
                                         QMessageBox.StandardButton.Yes |
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                # Reset game
                game.reset()
                for i in range(len(players)):
                    players[i].reset()
                    if i == 0:
                        self.sixth.player1Score.display(game.get_score(player=0))
                    elif i == 1:
                        self.sixth.player2Score.display(game.get_score(player=1))
                    else:
                        pass
                self.sixth.reset_buttons()
                self.num_turns = 0
            else:
                # Reset
                players[:] = []
                # Disconnect from imaging system
                disconnect()
                self.sixth.reset_buttons()
                self.sixth.reset_text()
                self.sixth.close()
                self.first.show()
        # Switch player
        else:
            if len(players) > 1 and self.num_turns == game.get_num_turns():
                self.num_turns = 0
                if player == 0:
                    self.sixth.player1Button.setEnabled(False)
                    self.sixth.player2Button.setEnabled(True)
                elif player == 1:
                    self.sixth.player1Button.setEnabled(True)
                    self.sixth.player2Button.setEnabled(False)
                else:
                    pass
            else:
                if player == 0:
                    self.sixth.player1Button.setEnabled(True)
                elif player == 1:
                    self.sixth.player2Button.setEnabled(True)
                else:
                    pass

    def player1_button(self):
        self.player_button(player=0)

    def player2_button(self):
        self.player_button(player=1)

    def quit_button(self):
        update_records()
        # Reset
        global game
        game = None
        players[:] = []
        disconnect()
        self.sixth.reset_buttons()
        self.sixth.reset_text()
        self.sixth.close()
        self.first.show()

def connect():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (constants.IP_ADDRESS, constants.PORT)
    client.connect(server_address)

def disconnect():
    client.send(constants.DONE_MSG.encode())
    client.close()

def update_records():
    date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    for i in range(len(players)):
        player_id = players[i].get_id()
        if player_id != 0:
            # Update number record table
            number_hits = players[i].get_number_hits()
            number_record = (date, player_id, game.get_id(), *number_hits)
            database.insert_number_record(number_record)
            # Update ring record table
            ring_hits = players[i].get_ring_hits()
            ring_record = (date, player_id, game.get_id(), *ring_hits)
            database.insert_ring_record(ring_record)
            # Update player table (throws, games, wins, id)
            num_throws = players[i].get_num_throws()
            num_games = players[i].get_num_games()
            num_wins = players[i].get_num_wins()
            player = (num_throws, num_games, num_wins, player_id)
            database.update_player(player)

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    ui = UserInterface()
    sys.exit(app.exec())

# EOF
