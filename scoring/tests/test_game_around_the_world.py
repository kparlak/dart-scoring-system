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

    def test_none_to_1(self):
        game = GameAroundTheWorld()
        self.assertEqual(game.update(player=0, number=1, ring='A'), 1, 'None to 1 is wrong')

if __name__ == '__main__':
    unittest.main()

# EOF
