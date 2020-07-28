import random

_VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
_SUITS = ['spades', 'clubs', 'diamonds', 'hearts']

class Cards:

    # Const for the deck and how many full decks should be used
    FULLDECK = []
    NUMDECKS = 4

    def __init__(self):
        for value in _VALUES:
            for suit in _SUITS:
                self.FULLDECK.append(f'{value} of {suit}')

        self.FULLDECK = self.FULLDECK * self.NUMDECKS
        self.currDeck = self.FULLDECK[:]

    # Picks a random card from the current deck, removes it,
    # and returns which card was picked
    def getCard(self) -> str:
        cardPicked = random.choice(self.currDeck)
        self.currDeck.remove(cardPicked)
        return cardPicked

    # Shuffles the cards by simply reassigning the current deck
    # to the full deck
    def shuffle(self) -> None:
        self.currDeck = self.FULLDECK[:]

    # Returns the size of the current deck
    def deckSize(self) -> int:
        return len(self.currDeck)

    # Returns number of full decks being used
    def getNumDecks(self) -> int:
        return self.NUMDECKS