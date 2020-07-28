from Player import Player
from Dealer import Dealer
from Cards import Cards
from Scoring import Scoring

class Game:

    # Constants for min bet, max bet, payout as a string, payout as a float, and when to shuffle
    MINBET = 20
    MAXBET = 500
    BLACKJACKPAYOUTSTR = '3:2'
    BLACKJACKPAYOUT = int(BLACKJACKPAYOUTSTR.split(':')[0]) / int(BLACKJACKPAYOUTSTR.split(':')[1])
    DEALER = Dealer()
    CARDS = Cards()
    SCORING = Scoring()
    WHENTOSHUFFLE = (CARDS.getNumDecks() * 52) // 3
    # WHENTOSHUFFLE is a const int that indicates how many cards need to be left before reshuffling the deck

    def __init__(self):
        self.players = []
        self.roundOver = True
        self.winnings = []

    def _determineWager(self, player: Player) -> int:
        """
        Private helper function that keeps prompting the player for a wager until they provide a valid input
        The wager input must be: an int, within the min/max bet range, no more than the amount of money they 
        have left
        """
        player_money = player.getMoney()
        wager_is_int = False

        # Accounting for user error of inputting anything other than an int for the wager.
        while not wager_is_int:
            try:
                # Covering the edge case of a player have less money left than the minimum bet.
                if player_money < self.MINBET:
                    print()
                    print(f'Since you currently have less money than the minimum bet (${self.MINBET}), you\'ll have to bet all your money!')
                    breakpoint = input('')
                    wager = player_money

                # Makes sure player bets within the range of the preset min and max bet.
                # Also, the player must have enough money left to make the bet.
                else:
                    wager = int(input(f'Please make a wager from ${self.MINBET} to ${self.MAXBET}: '))
                    while (wager < self.MINBET) or (wager > self.MAXBET) or (wager > player_money):
                        if wager < self.MINBET:
                            print(f'Sorry, you must bet at least ${self.MINBET}.')
                        elif wager > self.MAXBET:
                            print(f'Sorry, you can\'t bet more than ${self.MAXBET}.')
                        elif wager > player_money:
                            print('You don\'t have enough money to make that bet!')
                        print()
                        wager = int(input(f'Please make a wager from ${self.MINBET} to ${self.MAXBET}: '))
                wager_is_int = True

            except ValueError:
                print('Must give an int for your wager.')
                print()

        return wager

    def _determineInsuranceWager(self, player: Player) -> int:
        """
        Private helper function that keeps prompting the player for an insurance wager until they provide a valid input
        The insurance wager input must be: an int, at least $1 and no more than half their original wager, and it
        cannot be more than the amount of money the player has left (after their wage is deducted)
        """
        insurance_wager_is_int = False
        print(f'Total money left (after your wager of ${player.getWager()}): ${player.getMoney()-player.getWager()}')
        breakpoint = input('')

        # Accounting for user error of inputting anything other than an int for the wager.
        while not insurance_wager_is_int:
            try:
                insurance_wager = int(input(f'Please make an insurance wager from $1 to ${player.getWager() // 2} '))
                while (insurance_wager < 1) or (insurance_wager > player.getWager() // 2) or (player.getMoney() - player.getWager() - insurance_wager < 0):
                    if insurance_wager < 1:
                        print('Sorry, you can\'t wager anything less than $1.')
                    elif insurance_wager > player.getWager() // 2:
                        print(f'Sorry, you can\'t wager anything more than ${player.getWager() // 2}.')
                    else:
                        print('You don\'t have enough money to make that bet!')
                    print()
                    insurance_wager = int(input(f'Please make an insurance wager from $1 to ${player.getWager() // 2} '))
                insurance_wager_is_int = True

            except ValueError:
                print('Insurance wager must be an int.')
                print()

        return insurance_wager

    def addPlayer(self, player: Player) -> None:
        """
        Add a player to the game, but only after the round is over
        """
        if self.roundOver:
            self.players.append(player)

    # Removes a player from the game. Player is allowed to leave before
    # round is over, but they'll lose their wager.
    def removePlayer(self, player: Player) -> None:
        if player in self.players:
            self.players.remove(player)

    # Returns the current number of players
    def getNumPlayers(self) -> int:
        return len(self.players)

    # Returns a bool indicating whether the round is over or not
    def isRoundOver(self) -> bool:
        return self.roundOver

    # Uses the Scoring class to compare the player's hand to the dealer's
    # hand. Based on the winner and whether each person has a BlackJack,
    # the winnings (or losings) are determined for the player based on their
    # hand and their wager
    def determineWinnings(self) -> None:
        dealer_hand = self.DEALER.getHand()
        dealer_score = self.DEALER.getTotalScore()
        print('~~~~~~~~~~~~~~~Final Standings~~~~~~~~~~~~~~~')
        print(f'Dealer\'s final hand: {dealer_hand} === {dealer_score} points')
        breakpoint = input('')

        for player in self.players:
            for hand_num in range(1, player.getNumHands()+1):
                wager = player.getWager(hand_num)
                insurance_wager = player.getInsuranceWager()  # Might cause an error because of duplicate counting
                player_hand = player.getHand(hand_num)
                player_score = player.getTotalScore(hand_num)

                # If dealer gets a BlackJack, the player loses their wager unless they also have a BlackJack.
                # Also, they win twice their insurance wager if they chose to make one at the beginning of the round.
                if dealer_score == 21 and self.DEALER.handSize() == 2:
                    if player_score == 21 and player.handSize(hand_num) == 2:
                        winning = 0 + (insurance_wager * 2)
                    else:
                        winning = (wager * -1) + (insurance_wager * 2)

                # Payout for a BlackJack is based on the preset amount
                elif player_score == 21 and player.handSize(hand_num) == 2:
                    winning = int(wager * self.BLACKJACKPAYOUT) + (insurance_wager * -1)

                # If player busts, they lose their wager regardless of what hand the dealer has (even if dealer busts)
                elif player_score > 21:
                    winning = (wager * -1) + (insurance_wager * -1)

                # If the dealer busts or the player has a higher score than the dealer, they win their wager back
                elif dealer_score > 21 or player_score > dealer_score:
                    winning = wager + (insurance_wager * -1)

                # If neither the player nor dealer busts, but the player has a lower score than the dealer,
                # the player loses their wager.
                elif player_score < dealer_score:
                    winning = (wager * -1) + (insurance_wager * -1)

                # The last case is where the player has the same score as the dealer.
                else:
                    winning = 0 + (insurance_wager * -1)

                print(f'<{player.getName()}> Hand #{hand_num}: {player_hand} === {player_score} points | Winnings: {winning}')
                self.winnings.append((player, winning))
                breakpoint = input('')
        self.distributeWinnings()

    # Distributes all the winnings (or losings) back to the players and
    # changes their total money accordingly
    def distributeWinnings(self) -> None:
        for player, money in self.winnings:
            player.addMoney(money)

        # Kick a player out of the round if they're out of money
        for player in self.players[:]:
            if player.getMoney() <= 0:
                print(f'Sorry, {player.getName()}! You\'re out of money :( Thanks for playing!')
                self.removePlayer(player)
                breakpoint = input('')

        self.endRound()

    # Starts a new round and asks each player to make a wager before the cards are dealt.
    # New players are not allowed to join until the round is over.
    # Also, a round can't be started if there's no players in the game yet.
    def newRound(self) -> None:
        self.roundOver = False

        print()
        print('~~~~~~~~~~Welcome Challengers!~~~~~~~~~~')
        print(f'For this round we\'re using {self.CARDS.getNumDecks()} full decks and we have {len(self.players)} challengers playing.')
        print(f'The current number of cards left in the deck is {self.CARDS.deckSize()}')
        print(f'The deck will be reshuffled after {self.CARDS.deckSize() - self.WHENTOSHUFFLE} more cards are drawn')

        # For each player, print their name and total money, and then ask them to make a wager
        for player in self.players:
            print()
            print(f'Player: {player.getName()}')
            print(f'Total Money: ${player.getMoney()}')

            player.setWager(self._determineWager(player))

        print()
        print('~~~~~~~~~~Let the round begin. Good luck!~~~~~~~~~~')
        print()
        self.dealInitialCards()

    # Ends the round, clearing all of the hands and previous winnings
    def endRound(self) -> None:
        self.roundOver = True
        self.winnings = []

        # Shuffles the cards if necessary
        if self.CARDS.deckSize() <= self.WHENTOSHUFFLE:
            self.CARDS.shuffle()
            print('Shuffling cards...')
            breakpoint = input('')

        # Accounts for edge case that all the players lose their money and get kicked out of the game
        if self.getNumPlayers() > 0:
            print('~~~~~~~~~~~~~~~Everyone\'s Total Money~~~~~~~~~~~~~~~')
            for player in self.players:
                player.resetPlayer()
                print(f'{player.getName()}: ${player.getMoney()}')
        else:
            print('There\'s no more players left! Everyone ran out of money :(')

        self.DEALER.resetDealer()

        print()
        print('The round is over! Good game everyone!')
        breakpoint = input('')

    # Deals two cards to each player and then the dealer. Note that one
    # card is dealt to everyone before the second card is dealt.
    # I added 'breakpoint' variables for now to simulate dealing one card at a time.
    def dealInitialCards(self) -> None:
        self._dealPlayerInitialCards()
        self._dealDealerInitialCards()

        # All players have the option of making an insurance bet only if the dealer's first card is an Ace.
        if self.DEALER.getHand()[0][0] == 'A':
            self._insuranceBetting()

        self._dealPlayerInitialCards()
        self._dealDealerInitialCards()

        self.dealPlayerCards()

    # Helper function that deals one of the two initial cards to the player at the start of the round.
    def _dealPlayerInitialCards(self) -> None:
        for player in self.players:
            still_dealing = True
            while still_dealing:
                num_hands = player.getNumHands()
                for hand_num in range(1, num_hands+1):

                    # This is so we can skip the hands that already have two cards and only look at the rest that split.
                    if player.handSize(hand_num) != 2:
                        player.addCard(self.CARDS.getCard(), hand_num)
                        player_hand = player.getHand(hand_num)
                        player_score = self.SCORING.totalScore(player_hand)
                        print(f'<{player.getName()}> Hand #{hand_num}: {player_hand} === {player_score} points')

                        # Check to see if player wants to double down or split, but only if they have enough money to do so.
                        # Note, player cannot double down on a BlackJack.
                        if (player.handSize(hand_num) == 2) and (player.getWager(hand_num) + player.totalWager() <= player.getMoney()) and (player_score != 21):
                            print()
                            is_doubling_down = input('Want to double down? (Y/N) ')
                            while (is_doubling_down.upper() != 'Y') and (is_doubling_down.upper() != 'N'):
                                is_doubling_down = input('Want to double down? (Y/N) ')
                            print()

                            if is_doubling_down.upper() == 'Y':
                                player.doubleDown(hand_num)
                                print('Doubling down...')
                                breakpoint = input('')

                            # If player's two cards are identical, give them the choice to split.
                            # Note that the player cannot split to make more than 4 hands.
                            elif player_hand[0][0] == player_hand[1][0] and player.getNumHands() < 4:
                                is_splitting = input('Want to split? (Y/N) ')
                                while (is_splitting.upper() != 'Y') and (is_splitting.upper() != 'N'):
                                    is_splitting = input('Want to split? (Y/N) ')
                                print()

                                if is_splitting.upper() == 'Y':
                                    player.split(hand_num)
                                    print('Splitting hand...')
                                    breakpoint = input('')

                            if hand_num == player.getNumHands():
                                still_dealing = False

                        # Only stop dealing if we've successfully dealt two cards to all the hands.
                        elif hand_num == player.getNumHands():
                            still_dealing = False
                            breakpoint = input('')

                        # This is solely for printing purposes in the edge case that the user cannot split or double
                        # down due to lack of funds, and still has cards left to be dealt to their other hands.
                        elif player.handSize(hand_num) == 2:
                            breakpoint = input('')

                        player.setTotalScore(player_score, hand_num)

    # Helper function that deals one of the two initial cards to the dealer at the start of the round.
    def _dealDealerInitialCards(self) -> None:
        self.DEALER.addCard(self.CARDS.getCard())

        # Want to show only dealer's first card face up.
        if self.DEALER.handSize() == 1:
            dealer_hand = self.DEALER.getHand()
            dealer_score = self.SCORING.totalScore(dealer_hand)
            print(f'Dealer\'s hand: {dealer_hand} === {dealer_score} points')
        else:
            dealer_hand = [self.DEALER.getHand()[0], '?']
            dealer_score = self.SCORING.totalScore(self.DEALER.getHand())
            print(f'Dealer\'s hand: {dealer_hand} <= {self.SCORING.totalScore( [dealer_hand[0]] )} points')

        self.DEALER.setTotalScore(dealer_score)
        breakpoint = input('')

    # Helper function that asks players if they want to make an insurance bet.
    def _insuranceBetting(self) -> None:
        for player in self.players:
            # Accounts for edge case that player bet all their money and don't have any left for the insurance bet
            if player.getMoney() - player.getWager() == 0:
                print(f'Sorry, {player.getName()}! You don\'t have anymore money left to make an insurance bet :(')
                breakpoint = input('')
            else:
                insurance = input(f'{player.getName()}, care to make an insurance bet? (Y/N) ')
                while (insurance.upper() != 'Y') and (insurance.upper() != 'N'):
                    insurance = input(f'{player.getName()}, care to make an insurance bet? (Y/N) ')
                print()

                if insurance.upper() == 'Y':
                    player.setInsuranceWager(self._determineInsuranceWager(player))

    # Deals the rest of the cards to the players (depending on whether they choose
    # to hit or stand) and then to the dealer
    def dealPlayerCards(self) -> None:
        for player in self.players:
            print(f'~~~~~~~~~~~~~~~~{player.getName()}\'s Turn~~~~~~~~~~~~~~~~')
            print()

            for hand_num in range(1, player.getNumHands()+1):
                player_hand = player.getHand(hand_num)
                hand_score = player.getTotalScore(hand_num)

                # Check to see if the player has a BlackJack. Otherwise, proceed with their turn.
                if hand_score == 21:
                    print(f'Hand #{hand_num}: {player_hand} === {hand_score} points')
                    print()
                    print(f'Congrats, {player.getName()}! You got a BlackJack!')
                    breakpoint = input('')

                # If player doubled down on this hand, they only get one more card.
                elif player.hasDoubledDown(hand_num):
                    player.addCard(self.CARDS.getCard(), hand_num)
                    player_hand = player.getHand(hand_num)
                    hand_score = self.SCORING.totalScore(player_hand)

                    print('Since you doubled down on this hand, you only get one more card.')
                    breakpoint = input('')
                    print(f'Hand #{hand_num}: {player_hand} === {hand_score} points')
                    breakpoint = input('')

                    if hand_score > 21:
                        print(f'Sorry, {player.getName()}, this hand a bust!')
                        breakpoint = input('')

                else:
                    player.setTurn(True)

                while player.isTurn():
                    player_hand = player.getHand(hand_num)
                    hand_score = self.SCORING.totalScore(player_hand)
                    print(f'Hand #{hand_num}: {player_hand} === {hand_score} points')
                    print()

                    # If player busts, their turn is over.
                    if hand_score > 21:
                        print(f'Sorry, {player.getName()}, this hand is a bust!')
                        player.setTurn(False)
                        breakpoint = input('')

                    # Player cannot hit anymore when their hand gets to a score of 21.
                    elif hand_score == 21:
                        print(f'This hand is equal to 21, so you can\'t hit anymore')
                        player.setTurn(False)
                        breakpoint = input('')

                    else:
                        hit_or_stand = input('Would you like to hit or stand? ')

                        while (hit_or_stand.lower() != 'hit') and (hit_or_stand.lower() != 'stand'):
                            print('Must choose hit or stand.')
                            print()
                            hit_or_stand = input('Would you like to hit or stand? ')

                        if hit_or_stand.lower() == 'hit':
                            player.addCard(self.CARDS.getCard(), hand_num)
                            
                        else:
                            player.setTurn(False)
                            
                        print()
                        
                player.setTotalScore(hand_score, hand_num)
        self.dealDealerCards()

    # Dealer has their own set of rules for hitting and standing. Their decisions
    # are essentially made automatically: If the dealer's hand is 16 or less points, they
    # must hit. If their hand is 17 or more points, they must stand.
    def dealDealerCards(self) -> None:
        print('~~~~~~~~~~~~~~~~Dealer\'s Turn~~~~~~~~~~~~~~~~')
        print()

        dealer_hand = self.DEALER.getHand()
        dealer_score = self.DEALER.getTotalScore()

        if dealer_score == 21:
            print(f'Dealer\'s hand: {dealer_hand} === {dealer_score}')
            print()
            print(f'The dealer got a BlackJack!')
            breakpoint = input('')
        else:
            self.DEALER.setTurn(True)

        while self.DEALER.isTurn():
            dealer_hand = self.DEALER.getHand()
            dealer_score = self.SCORING.totalScore(dealer_hand)
            print(f'Dealer\'s hand: {dealer_hand} === {dealer_score}')
            breakpoint = input('')

            if dealer_score > 21:
                print('The dealer\'s hand is a bust!')
                self.DEALER.setTurn(False)
                
            elif dealer_score <= 16:
                print('The dealer chose to hit.')
                self.DEALER.addCard(self.CARDS.getCard())
                
            else:
                print('The dealer chose to stand.')
                self.DEALER.setTurn(False)
                
            breakpoint = input('')

        self.DEALER.setTotalScore(dealer_score)
        self.determineWinnings()

    # Returns the list of players who had winning hands
    def getWinners(self) -> [Player]:
        return [player for player, winning in self.winnings if winning > 0]

    # Returns the preset minimum bet
    def getMinBet(self) -> int:
        return self.MINBET

    # Returns the preset maximum bet
    def getMaxBet(self) -> int:
        return self.MAXBET

    # Returns the preset payout for getting a BlackJack
    def getPayout(self) -> float:
        return self.BLACKJACKPAYOUT

    # Returns the present payout for getting a BlackJack as a str
    def getPayoutStr(self) -> str:
        return self.BLACKJACKPAYOUTSTR
