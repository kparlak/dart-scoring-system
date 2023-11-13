#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   database.py
@Time    :   2023/11/13
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Class for database manipulation
'''

import sqlite3

class Database():
    def __init__(self):
        pass

    def connect_database(self, file):
        self.connection = None
        try:
            self.connection = sqlite3.connect(file)

        except sqlite3.Error as error:
            print(error)

        return self.connection

    def create_table(self, table):
        self.cursor = None
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(table)

        except sqlite3.Error as e:
            print(e)

    players_table = """CREATE TABLE IF NOT EXISTS players(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        name text NOT NULL,
                        username text NOT NULL,
                        num_games integer,
                        num_wins integer
                    );"""

    games_table =   """CREATE TABLE IF NOT EXISTS games(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        name text NOT NULL,
                        description text
                    );"""

    number_stats_table =    """CREATE TABLE IF NOT EXISTS number_stats(
                                player_id integer,
                                game_id integer,
                                date text NOT NULL,
                                num_1 integer,
                                num_2 integer,
                                num_3 integer,
                                num_4 integer,
                                num_5 integer,
                                num_6 integer,
                                num_7 integer,
                                num_8 integer,
                                num_9 integer,
                                num_10 integer,
                                num_11 integer,
                                num_12 integer,
                                num_13 integer,
                                num_14 integer,
                                num_15 integer,
                                num_16 integer,
                                num_17 integer,
                                num_18 integer,
                                num_19 integer,
                                num_20 integer,
                                FOREIGN KEY (player_id) REFERENCES players (id),
                                FOREIGN KEY (game_id) REFERENCES games (id)
                            );"""

    ring_stats_table =  """CREATE TABLE IF NOT EXISTS ring_stats(
                            player_id integer,
                            game_id integer,
                            date text NOT NULL,
                            num_single integer,
                            num_double integer,
                            num_triple integer,
                            num_bull integer,
                            num_bullseye integer,
                            FOREIGN KEY (player_id) REFERENCES players (id),
                            FOREIGN KEY (game_id) REFERENCES games (id)
                        );"""

    def insert_game(self, data):
        sql = '''INSERT INTO games(name, description)
                 VALUES(?, ?)
              '''
        cursor = self.connection.cursor()
        cursor.execute(sql, data)
        self.connection.commit()

    def insert_player(self, data):
        sql = '''INSERT INTO players(username, name)
                 VALUES(?, ?)
              '''
        cursor = self.connection.cursor()
        cursor.execute(sql, data)
        self.connection.commit()

    def select_game(self, data):
        sql = 'SELECT id FROM games WHERE name=?'
        cursor = self.connection.cursor()
        cursor.execute(sql, (data,))
        return cursor.fetchone()

    def select_player(self, data):
        sql = 'SELECT id FROM players WHERE username=?'
        cursor = self.connection.cursor()
        cursor.execute(sql, (data,))
        return cursor.fetchone()

    def insert_number_hit(self, data):
        sql = '''INSERT INTO number_stats(player_id, game_id, date, num_1, num_2, num_3, num_4, num_5, num_6, num_7, num_8, num_9, num_10, num_11, num_12, num_13, num_14, num_15, num_16, num_17, num_18, num_19, num_20)
                 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
              '''
        cursor = self.connection.cursor()
        cursor.execute(sql, data)
        self.connection.commit()

    def insert_ring_hit(self, data):
        sql = '''INSERT INTO ring_stats(player_id, game_id, date, num_single, num_double, num_triple, num_bull, num_bullseye)
                 VALUES(?, ?, ?, ?, ?, ?, ?, ?)
              '''
        cursor = self.connection.cursor()
        cursor.execute(sql, data)
        self.connection.commit()

# EOF
