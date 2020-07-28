from unittest import TestCase
from Game import Game
from Player import Player


class TestGame(TestCase):

    # Tests all the methods you can call before the game even starts
    def test_pre_game(self):
        g = Game()

        self.assertEqual(g.getNumPlayers(), 0)
        self.assertTrue(g.isRoundOver())

        # Makes sure error isn't thrown when trying to remove a player that isn't in the game
        g.removePlayer('Preston')

        p1 = Player('Preston')
        p2 = Player('Nicholas')
        g.addPlayer(p1)
        g.addPlayer(p2)
        self.assertEqual(g.getNumPlayers(), 2)

        g.removePlayer(p1)
        self.assertEqual(g.getNumPlayers(), 1)