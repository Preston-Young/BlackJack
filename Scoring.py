class Scoring:
    VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}

    def __init__(self):
        pass

    # Calculates the total score of a given hand
    def totalScore(self, hand: [str]) -> int:
        total = 0
        aces = 0

        # Don't count the aces until after counting all other cards. After, look at
        # the aces and decide whether to count them as 11 or 1
        for card in hand:

            # This is so we can ignore the suit of the card (i.e. '3 of hearts').
            # I wanted the first two characters for the edge case of '10 of XXXX'.
            # I used .strip() to take care of the white space for all the other values.
            value = card[0:2].strip()
            if value == 'A':
                aces += 1
            else:
                total += self.VALUES[value]

        for _ in range(aces):
            if total + 11 > 21:
                total += 1
            else:
                total += 11

        return total