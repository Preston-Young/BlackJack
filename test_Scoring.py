from unittest import TestCase
from Scoring import Scoring


class TestScoring(TestCase):

    # Tests to see if it returns a score of 0 for an empty hand
    def test_empty_hand(self):
        s = Scoring()
        self.assertEqual(s.totalScore([]), 0)

    # Tests a few hands without an ace in it
    def test_hands_without_ace(self):
        s = Scoring()

        self.assertEqual(s.totalScore(['3']), 3)
        self.assertEqual(s.totalScore(['J']), 10)
        self.assertEqual(s.totalScore(['10', 'Q']), 20)
        self.assertEqual(s.totalScore(['Q', '10']), 20)
        self.assertEqual(s.totalScore(['4', '8', 'K']), 22)

    # Tests a few hands with an ace in it
    def test_hands_with_ace(self):
        s = Scoring()

        self.assertEqual(s.totalScore(['A']), 11)
        self.assertEqual(s.totalScore(['4', 'A']), 15)
        self.assertEqual(s.totalScore(['A', 'K']), 21)
        self.assertEqual(s.totalScore(['7', '6', 'A']), 14)
        self.assertEqual(s.totalScore(['J', '10', 'A']), 21)
        self.assertEqual(s.totalScore(['9', 'A', '9']), 19)
        self.assertEqual(s.totalScore(['9', 'A', '9', 'J']), 29)
        self.assertEqual(s.totalScore(['9', 'A', 'A']), 21)
        self.assertEqual(s.totalScore(['9', 'A', '9', 'A']), 20)
        self.assertEqual(s.totalScore(['9', 'A', '7', 'A', '5']), 23)
        self.assertEqual(s.totalScore(['9', 'A', '9', 'A', 'A']), 21)
        self.assertEqual(s.totalScore(['A', 'A', 'A', 'A']), 14)