"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""

from Card import Deck, Hand, Card
from sets import Set


class PokerHand(Hand):

    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.

        Stores the result in attribute suits.
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1

    def rank_hist(self):
        """Builds a histogram of the ranks that appear in the hand.

        Stores the result in attribute ranks.
        """
        self.ranks = [0] * (len(Card.rank_names))
        for card in self.cards:
            self.ranks[card.rank] = self.ranks[card.rank] + 1

    def get_pairs(self):
        self.rank_hist()
        pairs = []
        for val in self.ranks:
            if val >= 2:
                pairs.append(val)
                if val == 4:
                    pairs.append(val)
        return pairs

    def has_pair(self):
        """Returns True if the hand has a pair, False otherwise.
        """
        return (len(self.get_pairs()) > 0)

    def has_two_pair(self):
        """Returns True if the hand has more than one pair, False otherwise.
        """
        return (len(self.get_pairs()) > 1)

    def has_three_of_kind(self):
        self.rank_hist()
        for val in self.ranks:
            if val >= 3:
                return True
        return False

    def has_straight(self):
        self.rank_hist()
        seq_count = 0
        for val in self.ranks:
            if val > 0:
                if seq_count is not 0:
                    seq_count += 1
                else:
                    seq_count = 1
            else:
                seq_count = 0

            if seq_count >= 5:
                return True

        if seq_count == 4 and self.ranks[1] > 0:
            return True
        return False

    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.

        Note that this works correctly for hands with more than 5 cards.
        """
        self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False

    def has_fullhouse(self):
        """Returns True if the hand has a full house, False otherwise.
        """
        self.rank_hist()
        pairs = Set()
        trips = Set()

        for val in self.ranks:
            if val >= 2:
                pairs.add(val)
                if val >= 3:
                    trips.add(val)
        if len(trips) > 0 and len(pairs - trips) > 0:
            return True
        return False

    def has_fourofkind(self):
        self.rank_hist()

        for val in self.ranks:
            if val == 4:
                return True
        return False

    def has_straightflush(self):
        # current_suit: value from 0 to 3
        card_iter = 0
        current_cards = []
        current_suit = self.cards[card_iter].suit
        current_cards.append(self.cards[card_iter])

        while card_iter < len(self.cards):
            while self.cards[card_iter].suit == current_suit:
                current_cards.append(self.cards[card_iter])
                card_iter += 1
                if card_iter == len(self.cards):
                    return False

            # Create a dummy Poker hand with all the cards of a suit
            dummy_hand = PokerHand()
            dummy_hand.cards = current_cards
            dummy_hand.sort()
            if dummy_hand.has_straight():
                return True

            current_cards = []
            current_suit = self.cards[card_iter].suit
            current_cards.append(self.cards[card_iter])
            card_iter += 1

        return False

    def classify(self):
        if self.has_straightflush():
            return 'Straight Flush'
        if self.has_fourofkind():
            return 'Four of a Kind'
        if self.has_fullhouse():
            return 'Full House'
        if self.has_flush():
            return 'Flush'
        if self.has_straight():
            return 'Straight'
        if self.has_three_of_kind():
            return 'Three of a Kind'
        if self.has_two_pair():
            return 'Two Pair'
        if self.has_pair():
            return 'Pair'


# Empty dict on purpose. Want to add to this as I go on
def single_run(hands={}):
    deck = Deck()
    deck.shuffle()

    # deal the cards and classify the hands
    for i in range(7):
        hand = PokerHand()
        deck.move_cards(hand, 7)
        hand.sort()
        classification = str(hand.classify())
        hands[classification] = hands.get(classification, 0) + 1

    return hands


def print_probabilities(hands):

    total = 0

    for val in hands:
        total += hands[val]

    print '**********************************************'
    print 'Poker Hand Probabilities'
    print '**********************************************'

    for val in hands:
        hands[val] = (hands[val] / float(total)) * 100

    for key in sorted(hands, key=hands.get, reverse=False):
        print '%s: %.2f %%' % (key, hands[key])

if __name__ == '__main__':
    # make a deck
    deck = Deck()
    deck.shuffle()

    # deal the cards and classify the hands
    for i in range(20000):
        hands = single_run()

    print_probabilities(hands)
