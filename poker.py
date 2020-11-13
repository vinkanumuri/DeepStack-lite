# TODO: add detailed comments


import random


class heads_up_holdem:
    def __init__(self, small_blind, big_blind, buy_in, hands=5, auto=False):
        p1 = human_io(buy_in)  # small blind in 1st hand
        p2 = human_io(buy_in)  # big blind in 1st hand
        hand(auto, [p1, p2], small_blind, big_blind, hands)

class hand:
    def __init__(self, auto, players, sblind, bblind, hands, hand_tracker=0):
        self.players, self.sblind, self.bblind, self.bet = players, sblind, bblind, bblind - sblind
        self.hands, self.hand_tracker, self.auto = hands, hand_tracker, auto
        self.pot, self.com, self.deck = 0, deck(not_com=False), deck()
        self.deal()

    def deal(self):
        for i in range(4):
            top = self.deck.cards.pop(0)
            self.players[(i + self.hand_tracker) % 2].pocket.append(top)
        self.preflop()

    def preflop(self):
        sb, bb = self.hand_tracker % 2, (self.hand_tracker + 1) % 2
        self.players[sb].chips, self.pot = self.players[0].chips - self.sblind, self.pot + self.sblind
        self.players[bb].chips, self.pot = self.players[1].chips - self.bblind, self.pot + self.bblind
        if self.auto:
            pass
        else:
            print('New hand: cards dealt and blinds added to pot.')
        self.betting(sb, self.bet)
        self.deck2com(3)  # flop then betting
        self.deck2com(1)  # turn then betting
        self.deck2com(1)  # river then betting
        self.showdown()

    def deck2com(self, cards):
        for c in range(cards):
            top = self.deck.cards.pop(0)
            self.com.cards.append(top)
        self.flop_turn_river()

    def flop_turn_river(self):
        sb, bb = self.hand_tracker % 2, (self.hand_tracker + 1) % 2
        if self.auto:
            pass
        else:
            self.printPlayerInfo(bb)
        print('test')
        self.betting(bb, self.bet)

    def betting(self, first, min_raise):
        if first == 0:
            second = 1
        elif first == 1:
            second = 0
        if self.auto:
            pass
        else:
            self.printPlayerInfo(first)
        first_bet = self.players[first].act(self.bet, min_raise)
        if first_bet == -1:
            self.reset(first)
        elif first_bet > self.bet:
            min_raise = 2 * (first_bet - self.bet) + self.bet
            self.bet = first_bet
        self.players[first].chips, self.pot = self.players[first].chips - self.bet, self.pot + self.bet
        #TODO: adjust self.bet, and ability to cycle on raise, check logic, error with small blind call
        if self.auto:
            pass
        else:
            self.printPlayerInfo(second)
        sec_bet = self.players[second].act(self.bet, min_raise)
        if sec_bet == -1:
            self.win(first)
        elif sec_bet > self.bet:
            min_raise = 2 * (sec_bet - self.bet) + self.bet
            self.bet = first_bet
        self.players[second].chips, self.pot = self.players[second].chips - sec_bet, self.pot + sec_bet
        if sec_bet > self.bet:
            self.bet = sec_bet
            self.betting(first, min_raise)


    def showdown(self):
        # TODO: compare hands and award pot, implement priced in for all-ins
        if self.auto:
            pass
        else:
            self.com.show()
            print('P1 pocket cards:')
            self.players[0].show()
            print('P2 pocket cards:')
            self.players[1].show()
        winner = input("who won? (0/1): ")
        self.reset(winner)

    def reset(self, winner):
        if self.auto:
            pass
        else:
            print('P' + str(winner+1) + ' won ' + str(self.pot))
        self.players[winner].chips += self.pot
        self.reset()
        if self.hand_tracker < self.hands:
            self.players[0].pocket, self.players[1].pocket = [], []
            hand(self.players, self.sblind, self.bblind, self.hands, hand_tracker=(self.hand_tracker + 1))

    def printPlayerInfo(self, p):
        if len(self.com.cards) != 0:
            print('Community cards:')
            self.com.show()
        print('P'+str(p + 1)+' pocket cards:')
        self.players[p].show()
        print('Pot: ' + str(self.pot))
        print('P1 chips: ' + str(self.players[0].chips))
        print('P2 chips: ' + str(self.players[1].chips))
        print('Player ' + str(p + 1) + "'s turn")


class deck:
    def __init__(self, not_com=True):
        self.cards = []
        if not_com:
            self.create()
            self.shuffle()

    def create(self):
        for r in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
            for s in ['H', 'C', 'D', 'S']:
                self.cards.append(card(r, s))

    def shuffle(self):
        random.shuffle(self.cards)

    def show(self):
        for c in self.cards:
            c.show()


class card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def show(self):
        print(self.rank, self.suit)


class player:
    def __init__(self, buyin):
        self.pocket = []
        self.chips = buyin

    def show(self):
        for c in self.pocket:
            c.show()

    # def buy_in(self, amount):
    #     pass
    #
    # def cash_out(self):
    #     pass


class human_io(player):
    def __init__(self, buy_in):
        player.__init__(self, buy_in)

    def act(self, bet, min_raise):
        if bet == 0:
            print('fold: -1 | check: 0 | min-raise: 0 | all in: '+str(self.chips))
        else:
            print('fold: -1 | call: ' + str(bet) + ' | min-raise: ' + str(min_raise) + ' | all in: '+str(self.chips))
        # TODO: all in pot split functionality
        play = int(input('play: '))
        if play == -1:
            print('Player folded')
        elif play == 0 and bet == 0:
            print('Player checked')
        elif play == bet and play < self.chips:
            print('Player called ' +str(play))
        elif play > min_raise and play < self.chips:
            print('Player raised to ' + str(play))
        elif play == self.chips:
            print('Player all in '+str(play))
        else:
            print('Invalid input!')
            self.act(bet)
        return play


#  testing
heads_up_holdem(5000, 10000, 1000000, 5)











