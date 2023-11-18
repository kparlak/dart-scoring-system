#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   game_501.py
@Time    :   2023/11/05
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Class for '501' game
'''

import array as arr

class Game501():
    def __init__(self):
        self.reset()

    def reset(self):
        self.score = arr.array('i', [501, 501])
        self.winner = arr.array('b', [False, False])

    def get_num_turns(self):
        return 3

    def get_num_players(self):
        return len(self.score)

    def set_score(self, player, score):
        self.score[player] = score

    def get_score(self, player):
        return self.score[player]

    def get_winner(self, player):
        return bool(self.winner[player])

    def calc_hit(self, number, ring):
        if ring == 'B' or ring == 'D':
            return number
        elif ring == 'A':
            return number * 2
        elif ring == 'C':
            return number * 3
        elif ring == 'X':
            return 25
        elif ring == 'Y':
            return 50
        else:
            return 0

    def update(self, player, number, ring):
        hit = self.calc_hit(number, ring)
        temp_score = self.score[player] - hit
        if temp_score < 0:
            return self.score[player]
        elif temp_score == 0:
            if ring == 'A' or number == 1:
                self.winner[player] = True
                self.score[player] = temp_score
                return self.score[player]
            else:
                return self.score[player]
        else: # temp_score > 0
            self.score[player] = temp_score
            return self.score[player]

# EOF
