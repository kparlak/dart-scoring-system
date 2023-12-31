#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   test_game_501.py
@Time    :   2023/11/05
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Class for testing '501' game class
'''

import unittest
import sys
sys.path.append("..")

from game_501 import Game501

class TestGame501(unittest.TestCase):

    def test_hit_double(self):
        game = Game501()
        self.assertEqual(game.update(player=0, number=20, ring='A'), 461, 'Double ring hit is wrong')

    def test_hit_single_upper(self):
        game = Game501()
        self.assertEqual(game.update(player=0, number=20, ring='B'), 481, 'Single upper ring hit is wrong')

    def test_hit_triple(self):
        game = Game501()
        self.assertEqual(game.update(player=0, number=20, ring='C'), 441, 'Triple ring hit is wrong')

    def test_hit_single_lower(self):
        game = Game501()
        self.assertEqual(game.update(player=0, number=20, ring='D'), 481, 'Single lower ring hit is wrong')

    def test_hit_bull(self):
        game = Game501()
        self.assertEqual(game.update(player=0, number=20, ring='X'), 476, 'Bull hit is wrong')

    def test_hit_bullseye(self):
        game = Game501()
        self.assertEqual(game.update(player=0, number=20, ring='Y'), 451, 'Bullseye hit is wrong')

    def test_hit_zero(self):
        game = Game501()
        self.assertEqual(game.update(player=0, number=20, ring='Z'), 501, 'Zero hit is wrong')

    def test_score_below_zero(self):
        game = Game501()
        game.set_score(player=0, score=20)
        self.assertEqual(game.update(player=0, number=20, ring='A'), 20, 'Below zero score is wrong')

    def test_score_winner_zero_single(self):
        game = Game501()
        game.set_score(player=0, score=20)
        self.assertEqual(game.update(player=0, number=20, ring='B'), 20, 'Zero score with single hit is wrong')
        self.assertEqual(game.get_winner(player=0), False, 'Winner declaration is wrong')

    def test_score_winner_zero_double(self):
        game = Game501()
        game.set_score(player=0, score=20)
        self.assertEqual(game.update(player=0, number=10, ring='A'), 0, 'Zero score with double hit is wrong')
        self.assertEqual(game.get_winner(player=0), True, 'Winner declaration is wrong')

if __name__ == '__main__':
    unittest.main()

# EOF
