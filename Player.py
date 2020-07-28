class Player:
    STARTINGFUNDS = 1000

    def __init__(self, name):
        self.name = name
        self.money = self.STARTINGFUNDS
        self.wager = [0]
        self.insurance_wager = 0
        self.hand = [[]]
        self.totalScore = [0]
        self.turn = False
        self.double_down = [False]

    # Returns player name
    def getName(self) -> str:
        return self.name

    # Returns player money
    def getMoney(self) -> int:
        return self.money

    # Sets the player's wager for a given hand
    def setWager(self, wager: int, hand_num: int = 1) -> None:
        self.wager[hand_num-1] = wager

    # Returns player wager for a given hand
    def getWager(self, hand_num: int = 1) -> int:
        return self.wager[hand_num-1]

    # Returns total amount of money the player wagered
    def totalWager(self) -> int:
        return sum(self.wager) + self.insurance_wager

    # A player can place a side insurance bet up to half of their original wager that
    # the dealer will have a "blackjack." If the dealer indeed has a "blackjack," the
    # player will receive twice the amount they wagered for this side bet and their
    # original wager gets treated under the normal BlackJack rules. Players only get the
    # option to make this bet if the dealer's face-up card is specifically an Ace.
    def setInsuranceWager(self, wager: int) -> None:
        self.insurance_wager = wager

    # Returns player insurance wager
    def getInsuranceWager(self) -> int:
        return self.insurance_wager

    # Returns the player's hand(s) (hands if player chose to split)
    def getHand(self, hand_num: int = 1) -> [str]:
        return self.hand[hand_num-1]

    # Returns size of player's hand(s) (hands if player chose to split)
    def handSize(self, hand_num: int = 1) -> int:
        return len(self.hand[hand_num-1])

    # Returns the number of hands the player currently has.
    def getNumHands(self) -> int:
        return len(self.hand)

    # Sets the total score of the player's hand(s) (hands if player chose to split)
    def setTotalScore(self, score: int, hand_num: int = 1) -> None:
        self.totalScore[hand_num-1] = score

    # Returns total score of player's hand(s) (hands if player chose to split)
    def getTotalScore(self, hand_num: int = 1) -> int:
        return self.totalScore[hand_num-1]

    # Sets the player's turn to true or false
    def setTurn(self, is_turn: bool) -> None:
        self.turn = is_turn

    # Returns whether or not it's the player's turn
    def isTurn(self) -> bool:
        return self.turn

    # Adds a card to player's hand(s) (hands if player chose to split)
    def addCard(self, card: str, hand_num: int = 1) -> None:
        self.hand[hand_num-1].append(card)

    # Adds winnings (or subtracts losings) to player's total money
    def addMoney(self, money) -> None:
        self.money += money

    # Player can split into two hands if both original cards have identical values.
    # Note that the player can split to make up to four individual hands.
    def split(self, hand_num: int = 1) -> None:
        card = self.hand[hand_num-1].pop(0)
        self.hand.append([card])
        self.wager.append(self.wager[hand_num-1])
        self.totalScore.append(0)
        self.double_down.append(False)

    # Some variations allow the player to double down when original two cards total up to 9, 10, or 11
    # I'm always allowing players to double down on their first two cards. However, when doubling down,
    # the player is only allowed on more card and cannot hit anymore. Note that a player may double down
    # on split hands.
    def doubleDown(self, hand_num: int = 1) -> None:
        self.double_down[hand_num-1] = True
        self.wager[hand_num-1] *= 2

    # Returns whether or not player doubled down for a given hand(s) (hands if the player chose to split)
    def hasDoubledDown(self, hand_num: int = 1) -> bool:
        return self.double_down[hand_num-1]

    # Returns the preset starting funds
    def getStartingFunds(self) -> int:
        return self.STARTINGFUNDS

    # Resets the necessary attributes after the round is over
    def resetPlayer(self) -> None:
        self.wager = [0]
        self.insurance_wager = 0
        self.hand = [[]]
        self.totalScore = [0]
        self.double_down = [False]
