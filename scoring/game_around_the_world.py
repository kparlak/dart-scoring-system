#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   game_around_the_world.py
@Time    :   2023/11/05
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Class for 'Around the World' game
'''

import array as arr

class GameAroundTheWorld():
    def __init__(self):
        self.score = arr.array('i', [0, 0])
        self.winner = arr.array('b', [False, False])

    def get_num_players(self):
        return len(self.score)

    def set_score(self, player, score):
        self.score[player] = score

    def get_score(self, player):
        return self.score[player]

    def get_winner(self, player):
        return bool(self.winner[player])

    def update(self, player, number, ring):
        if ring == 'A' or ring == 'B' or ring == 'C' or ring == 'D':
            if self.score[player] == 0 and number == 1:
                self.score[player] = number
            elif self.score[player] == 1 and number == 18:
                self.score[player] = number
            elif self.score[player] == 18 and number == 4:
                self.score[player] = number
            elif self.score[player] == 4 and number == 13:
                self.score[player] = number
            elif self.score[player] == 13 and number == 6:
                self.score[player] = number
            elif self.score[player] == 6 and number == 10:
                self.score[player] = number
            elif self.score[player] == 10 and number == 15:
                self.score[player] = number
            elif self.score[player] == 15 and number == 2:
                self.score[player] = number
            elif self.score[player] == 2 and number == 17:
                self.score[player] = number
            elif self.score[player] == 17 and number == 3:
                self.score[player] = number
            elif self.score[player] == 3 and number == 19:
                self.score[player] = number
            elif self.score[player] == 19 and number == 7:
                self.score[player] = number
            elif self.score[player] == 7 and number == 16:
                self.score[player] = number
            elif self.score[player] == 16 and number == 8:
                self.score[player] = number
            elif self.score[player] == 8 and number == 11:
                self.score[player] = number
            elif self.score[player] == 11 and number == 14:
                self.score[player] = number
            elif self.score[player] == 14 and number == 9:
                self.score[player] = number
            elif self.score[player] == 9 and number == 12:
                self.score[player] = number
            elif self.score[player] == 12 and number == 5:
                self.score[player] = number
            elif self.score[player] == 5 and number == 20:
                self.score[player] = number
                self.winner[player] = True

        return self.score[player]

# EOF
