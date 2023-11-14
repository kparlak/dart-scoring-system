#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   run_database.py
@Time    :   2023/11/13
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Runs queries and inserts of the database
'''

import sys
sys.path.append("..")

from database import Database
from datetime import datetime

database = Database()
database.connect('../DARTS.db')

# Create tables
# database.create_table(database.players_table)
# database.create_table(database.games_table)
# database.create_table(database.ring_records_table)
# database.create_table(database.number_records_table)

# Insert game
# game = ("501", "Start with score of 501 and reach zero")
# database.insert_game(game)
# game = ("Around the World", "Start at 1 and hit numbers sequentially clockwise around the board")
# database.insert_game(game)

# Insert player
# player = ("kevin5176", "Kevin Parlak", 0, 0)
# database.insert_player(player)
# player = ("jamie712", "Jamie Parlak", 0, 0)
# database.insert_player(player)

# Insert number record
# time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
# number_record = (time, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
# database.insert_number_record(number_record)
# number_record = (time, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
# database.insert_number_record(number_record)

# Insert ring record
# time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
# ring_record = (time, 1, 1, 0, 0, 0, 0, 0)
# database.insert_ring_record(ring_record)
# ring_record = (time, 2, 1, 0, 0, 0, 0, 0)
# database.insert_ring_record(ring_record)

# Select game
# game = database.select_game("501")
# if game == None:
#     print('Game does not exist')
# else:
#     print(game[0])

# Select player
# player = database.select_player("kevin5176")
# if player == None:
#     print('Player does not exist')
# else:
#     print(player[0][1])

# Update player
# player = (4, 4, 1)
# database.update_player(player)

# EOF
