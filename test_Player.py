from unittest import TestCase
from Player import Player


class TestPlayer(TestCase):

    # Tests that the simple methods return their correct information
    def test_get_methods(self):

        p = Player('Preston')
        self.assertEqual(p.getName(), 'Preston')
        self.assertEqual(p.getMoney(), p.STARTINGFUNDS)
        self.assertEqual(p.getWager(), 0)
        self.assertEqual(p.getInsuranceWager(), 0)
        self.assertEqual(p.getHand(), [])
        self.assertEqual(p.getTotalScore(), 0)
        self.assertEqual(p.handSize(), 0)
        self.assertFalse(p.isTurn())

    # Tests addMoney() and addCard() methods
    def test_add_methods(self):
        p1 = Player('Preston')
        p1.addMoney(45)
        p1.addCard('4')

        self.assertEqual(p1.getMoney(), p1.STARTINGFUNDS + 45)
        self.assertEqual(p1.getHand(), ['4'])
        self.assertEqual(p1.handSize(), 1)

        p2 = Player('Nicholas')
        p2.addMoney(45)
        p2.addMoney(-45)
        p2.addCard('4')
        p2.addCard('J')
        p2.addCard('A')

        self.assertEqual(p2.getMoney(), p2.STARTINGFUNDS)
        self.assertEqual(p2.getHand(), ['4', 'J', 'A'])
        self.assertEqual(p2.handSize(), 3)

    # Tests split method
    def test_split(self):
        p = Player('Preston')
        p.addCard('8')
        p.addCard('8')
        p.split()

        self.assertEqual(p.getHand(), ['8'])
        self.assertEqual(p.getHand(1), ['8'])
        self.assertEqual(p.getHand(2), ['8'])