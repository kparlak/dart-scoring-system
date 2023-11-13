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
database.connect_database('DARTS.db')

# Create tables
# database.create_table(database.players_table)
# database.create_table(database.games_table)
# database.create_table(database.ring_stats_table)
# database.create_table(database.number_stats_table)

# Insert games
# game = ("501", "Start with score of 501 and reach zero")
# database.insert_game(game)
# game = ("Around the World", "Start at 1 and hit numbers sequentially clockwise around the board")
# database.insert_game(game)

# Insert players
# player = ("kevin5176", "Kevin Parlak")
# database.insert_player(player)
# player = ("jamie712", "Jamie Parlak")
# database.insert_player(player)

# Select game
# game = database.select_game("501")
# if game == None:
#     print('Game does not exist')
# else:
#     print(game[0])

# Select players
# player = database.select_player("kevin5176")
# if player == None:
#     print('Player does not exist')
# else:
#     print(player[0])

# Insert number hits
# time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
# number_hit = (1, 1, time, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
# database.insert_number_hit(number_hit)
# number_hit = (2, 1, time, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
# database.insert_number_hit(number_hit)

# Insert ring hits
# time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
# ring_hit = (1, 1, time, 0, 0, 0, 0, 0)
# database.insert_ring_hit(ring_hit)
# ring_hit = (2, 1, time, 0, 0, 0, 0, 0)
# database.insert_ring_hit(ring_hit)

# EOF
