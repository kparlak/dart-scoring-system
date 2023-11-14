#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   player.py
@Time    :   2023/11/13
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Class for player statistics
'''

class Player():
    def __init__(self, id):
        self.id = id
        self.num_single = 0
        self.num_double = 0
        self.num_triple = 0
        self.num_bull = 0
        self.num_bullseye = 0
        self.num_1 = 0
        self.num_2 = 0
        self.num_3 = 0
        self.num_4 = 0
        self.num_5 = 0
        self.num_6 = 0
        self.num_7 = 0
        self.num_8 = 0
        self.num_9 = 0
        self.num_10 = 0
        self.num_11 = 0
        self.num_12 = 0
        self.num_13 = 0
        self.num_14 = 0
        self.num_15 = 0
        self.num_16 = 0
        self.num_17 = 0
        self.num_18 = 0
        self.num_19 = 0
        self.num_20 = 0

    def get_id(self):
        return self.id

    def get_ring_hits(self):
        return (self.num_single, self.num_double, self.num_triple,
                self.num_bull, self.num_bullseye)

    def get_number_hits(self):
        return (self.num_1, self.num_2, self.num_3, self.num_4, self.num_5,
                self.num_6, self.num_7, self.num_8, self.num_9, self.num_10,
                self.num_11, self.num_12, self.num_13, self.num_14, self.num_15,
                self.num_16, self.num_17, self.num_18, self.num_19, self.num_20)

    def update_ring(self, ring):
        if ring == 'B' or ring == 'D':
            self.num_single += 1
        elif ring == 'A':
            self.num_double += 1
        elif ring == 'C':
            self.num_triple += 1
        elif ring == 'X':
            self.num_bull += 1
        elif ring == 'Y':
            self.num_bullseye += 1

    def update_number(self, number):
        if number == 1:
            self.num_1 += 1
        elif number == 2:
            self.num_2 += 1
        elif number == 3:
            self.num_3 += 1
        elif number == 4:
            self.num_4 += 1
        elif number == 5:
            self.num_5 += 1
        elif number == 6:
            self.num_6 += 1
        elif number == 7:
            self.num_7 += 1
        elif number == 8:
            self.num_8 += 1
        elif number == 9:
            self.num_9 += 1
        elif number == 10:
            self.num_10 += 1
        elif number == 11:
            self.num_11 += 1
        elif number == 12:
            self.num_12 += 1
        elif number == 13:
            self.num_13 += 1
        elif number == 14:
            self.num_14 += 1
        elif number == 15:
            self.num_15 += 1
        elif number == 16:
            self.num_16 += 1
        elif number == 17:
            self.num_17 += 1
        elif number == 18:
            self.num_18 += 1
        elif number == 19:
            self.num_19 += 1
        elif number == 20:
            self.num_20 += 1

# EOF
