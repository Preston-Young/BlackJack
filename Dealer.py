class Dealer:

    def __init__(self):
        self.hand = []
        self.totalScore = 0
        self.turn = False

    # Return whether or not it's the dealer's turn
    def isTurn(self) -> bool:
        return self.turn

    # Sets the dealer's turn to true or false
    def setTurn(self, is_turn: bool) -> None:
        self.turn = is_turn

    # Return the dealer's current hand
    def getHand(self) -> [str]:
        return self.hand

    # Sets the dealer's total score of the dealer's hand
    def setTotalScore(self, score: int) -> None:
        self.totalScore = score

    # Returns the total score of the dealer's hand
    def getTotalScore(self) -> int:
        return self.totalScore

    # Adds a card to the dealer's hand
    def addCard(self, card: str) -> None:
        self.hand.append(card)

    # Returns the dealer's current hand size
    def handSize(self) -> int:
        return len(self.hand)

    # Resets the necessary attributes after the round is over
    def resetDealer(self) -> None:
        self.hand = []
        self.totalScore = 0