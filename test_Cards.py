from unittest import TestCase
from Cards import Cards


class TestCards(TestCase):

    # Tests if initial deck contains 4 full decks
    def test_full_deck(self):

        c = Cards()

        self.assertEqual(c.FULLDECK, ['2 of spades', '2 of clubs', '2 of diamonds', '2 of hearts',
                                      '3 of spades', '3 of clubs', '3 of diamonds', '3 of hearts',
                                      '4 of spades', '4 of clubs', '4 of diamonds', '4 of hearts',
                                      '5 of spades', '5 of clubs', '5 of diamonds', '5 of hearts',
                                      '6 of spades', '6 of clubs', '6 of diamonds', '6 of hearts',
                                      '7 of spades', '7 of clubs', '7 of diamonds', '7 of hearts',
                                      '8 of spades', '8 of clubs', '8 of diamonds', '8 of hearts',
                                      '9 of spades', '9 of clubs', '9 of diamonds', '9 of hearts',
                                      '10 of spades', '10 of clubs', '10 of diamonds', '10 of hearts',
                                      'J of spades', 'J of clubs', 'J of diamonds', 'J of hearts',
                                      'Q of spades', 'Q of clubs', 'Q of diamonds', 'Q of hearts',
                                      'K of spades', 'K of clubs', 'K of diamonds', 'K of hearts',
                                      'A of spades', 'A of clubs', 'A of diamonds', 'A of hearts'] * c.getNumDecks())
        self.assertEqual(c.FULLDECK, c.currDeck)
        self.assertEqual(c.deckSize(), len(c.FULLDECK))

    # Tests to see if drawing a card decreases the size of the current deck by one
    def test_get_card(self):

        c = Cards()
        c.getCard()

        self.assertNotEqual(c.currDeck, c.FULLDECK)
        self.assertNotEqual(c.deckSize(), len(c.FULLDECK))

    # Tests to see if shuffle brings the deck back to 4 full decks
    def test_shuffle(self):

        c = Cards()
        c.getCard()
        c.shuffle()

        self.assertEqual(c.currDeck, c.FULLDECK)