#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   test_game_around_the_world.py
@Time    :   2023/11/05
@Author  :   Kevin Parlak
@Version :   1.0
@License :   MIT
@Desc    :   Class for testing 'Around the World' game class
'''

import unittest
import sys
sys.path.append("..")

from game_around_the_world import GameAroundTheWorld

class TestGameAroundTheWorld(unittest.TestCase):

    def test_hit_double(self):
        game = GameAroundTheWorld()
        self.assertEqual(game.update(player=0, number=1, ring='A'), 1, 'Double ring hit is wrong')

    def test_hit_single_upper(self):
        game = GameAroundTheWorld()
        self.assertEqual(game.update(player=0, number=1, ring='B'), 1, 'Single upper ring hit is wrong')

    def test_hit_triple(self):
        game = GameAroundTheWorld()
        self.assertEqual(game.update(player=0, number=1, ring='C'), 1, 'Triple ring hit is wrong')

    def test_hit_single_lower(self):
        game = GameAroundTheWorld()
        self.assertEqual(game.update(player=0, number=1, ring='D'), 1, 'Single lower ring hit is wrong')

    def test_hit_bull(self):
        game = GameAroundTheWorld()
        self.assertEqual(game.update(player=0, number=1, ring='X'), 0, 'Bull hit is wrong')

    def test_hit_bullseye(self):
        game = GameAroundTheWorld()
        self.assertEqual(game.update(player=0, number=1, ring='Y'), 0, 'Bullseye hit is wrong')

    def test_hit_zero(self):
        game = GameAroundTheWorld()
        self.assertEqual(game.update(player=0, number=1, ring='Z'), 0, 'Zero hit is wrong')

    def test_score_zero_hit_20(self):
        game = GameAroundTheWorld()
        self.assertEqual(game.update(player=0, number=20, ring='A'), 0, 'Score of 0 hitting 20 is wrong')

    def test_score_1_hit_18(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=1)
        self.assertEqual(game.update(player=0, number=18, ring='A'), 18, 'Score of 1 hitting 18 is wrong')

    def test_score_18_hit_4(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=18)
        self.assertEqual(game.update(player=0, number=4, ring='A'), 4, 'Score of 18 hitting 4 is wrong')

    def test_score_4_hit_13(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=4)
        self.assertEqual(game.update(player=0, number=13, ring='A'), 13, 'Score of 4 hitting 13 is wrong')

    def test_score_13_hit_6(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=13)
        self.assertEqual(game.update(player=0, number=6, ring='A'), 6, 'Score of 13 hitting 6 is wrong')

    def test_score_6_hit_10(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=6)
        self.assertEqual(game.update(player=0, number=10, ring='A'), 10, 'Score of 6 hitting 10 is wrong')

    def test_score_10_hit_15(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=10)
        self.assertEqual(game.update(player=0, number=15, ring='A'), 15, 'Score of 10 hitting 15 is wrong')

    def test_score_15_hit_2(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=15)
        self.assertEqual(game.update(player=0, number=2, ring='A'), 2, 'Score of 15 hitting 2 is wrong')

    def test_score_2_hit_17(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=2)
        self.assertEqual(game.update(player=0, number=17, ring='A'), 17, 'Score of 2 hitting 17 is wrong')

    def test_score_17_hit_3(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=17)
        self.assertEqual(game.update(player=0, number=3, ring='A'), 3, 'Score of 17 hitting 3 is wrong')

    def test_score_3_hit_19(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=3)
        self.assertEqual(game.update(player=0, number=19, ring='A'), 19, 'Score of 3 hitting 19 is wrong')

    def test_score_19_hit_7(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=19)
        self.assertEqual(game.update(player=0, number=7, ring='A'), 7, 'Score of 19 hitting 7 is wrong')

    def test_score_7_hit_16(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=7)
        self.assertEqual(game.update(player=0, number=16, ring='A'), 16, 'Score of 7 hitting 16 is wrong')

    def test_score_16_hit_8(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=16)
        self.assertEqual(game.update(player=0, number=8, ring='A'), 8, 'Score of 16 hitting 8 is wrong')

    def test_score_8_hit_11(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=8)
        self.assertEqual(game.update(player=0, number=11, ring='A'), 11, 'Score of 8 hitting 11 is wrong')

    def test_score_11_hit_14(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=11)
        self.assertEqual(game.update(player=0, number=14, ring='A'), 14, 'Score of 11 hitting 14 is wrong')

    def test_score_14_hit_9(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=14)
        self.assertEqual(game.update(player=0, number=9, ring='A'), 9, 'Score of 14 hitting 9 is wrong')

    def test_score_9_hit_12(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=9)
        self.assertEqual(game.update(player=0, number=12, ring='A'), 12, 'Score of 9 hitting 12 is wrong')

    def test_score_12_hit_5(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=12)
        self.assertEqual(game.update(player=0, number=5, ring='A'), 5, 'Score of 12 hitting 5 is wrong')

    def test_winner(self):
        game = GameAroundTheWorld()
        game.set_score(player=0, score=5)
        self.assertEqual(game.update(player=0, number=20, ring='A'), 20, 'Score of 5 hitting 20 is wrong')
        self.assertEqual(game.get_winner(player=0), True, 'Winner declaration is wrong')

if __name__ == '__main__':
    unittest.main()

# EOF
