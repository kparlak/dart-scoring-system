#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   initialize_database.py
@Time    :   2023/11/14
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Initializes database and tables
'''

from database import Database

database = Database()

database.connect('/data/DARTS.db')

# Create tables
database.create_table(database.players_table)
database.create_table(database.games_table)
database.create_table(database.ring_records_table)
database.create_table(database.number_records_table)

# Insert game
game = ("501", "Score based game where the player starts with a score of 501 and must reach zero")
database.insert_game(game)
game = ("Around the World", "Knockout based game where the player starts at 1 and must hit numbers sequentially in clockwise order around the board")
database.insert_game(game)

# EOF
