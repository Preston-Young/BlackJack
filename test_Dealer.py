from unittest import TestCase
from Dealer import Dealer
from Scoring import Scoring


class TestDealer(TestCase):

    # Tests some of the inital conditions of a dealer before the game starts
    def test_pre_game(self):
        d = Dealer()

        self.assertFalse(d.isTurn())
        self.assertEqual(d.getHand(), [])
        self.assertEqual(d.getTotalScore(), 0)
        self.assertEqual(d.handSize(), 0)

    # Tests adding a few cards
    def test_add_cards(self):
        s = Scoring()

        d1 = Dealer()
        d1.addCard('4')
        d1.setTotalScore(s.totalScore(['4']))

        self.assertEqual(d1.getHand(), ['4'])
        self.assertEqual(d1.handSize(), 1)
        self.assertEqual(d1.getTotalScore(), 4)

        d2 = Dealer()
        d2.addCard('3')
        d2.addCard('J')
        d2.addCard('7')
        d1.setTotalScore(s.totalScore(['3', 'J', '7']))

        self.assertEqual(d2.getHand(), ['3', 'J', '7'])
        self.assertEqual(d2.handSize(), 3)
        self.assertEqual(d1.getTotalScore(), 20)