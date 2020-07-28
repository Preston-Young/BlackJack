from Game import Game
from Player import Player

if __name__ == '__main__':
    g = Game()
    print(f'~~~~~~~Welcome to Preston\'s BlackJack! The current payout for a BlackJack is {g.getPayoutStr()}~~~~~~~')
    print()

    # Essentially right now this is a while True loop
    while g.isRoundOver():
        player = input('Please enter the name of the new challenger (Press Enter if there aren\'t any): ')
        if player != '':
            g.addPlayer(Player(player))

        if g.getNumPlayers() > 0:
            can_start = input('Ready to start? If not, let\'s add more challengers! (Y/N) ')
            while (can_start.upper() != 'Y') and (can_start.upper() != 'N'):
                can_start = input('Ready to start? If not, let\'s add more challengers! (Y/N) ')
            if can_start.upper() == 'Y':
                g.newRound()
        else:
            print('Cannot start a round. There aren\'t any players :(')
        print()