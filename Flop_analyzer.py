from enum import Enum
from functools import partial
import itertools
from abc import ABC

VALUES = Enum('VALUES', 'TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN JACK QUEEN KING ACE')
SUITS = Enum('SUITS', 'HEARTS SPADES DIAMONDS CLUBS')

def is_straight(hand_values):
    """check for a straight"""
    hand_values = [card.value for card in hand_values] #create a list of integer values for each card in the hand
    
    if not len(hand_values) == len(set(hand_values)) == 5: # returns false if the list is not 5 unique values
        return False
    
    hand_values.sort()
    if (hand_values[-1] == hand_values[0]+4 or hand_values == [2,3,4,5,14]):
        return True
    return False


def is_flush(suits):
    """check for a flush"""
    suits = [suit.value for suit in suits]
    if len(set(suits)) == 1:
        return True
    return False


def five_different_values(hand_values, hand_suits):
    """
    checks hands where 5 cards have different values for straights, flushes and straight flushes
    """
    if is_flush(hand_suits):
        if is_straight(hand_values):
            return 'straight flush'
        else:
            return 'flush'

    elif is_straight(hand_values):
        return 'straight'
    
    else:
        return 'missed'
    

def four_different_values(hole_card_values, flop_values):
    """ 
    Takes hands where there is one pair and determines whether the hole cards have hit top pair,
    middle pair or bottom pair.
    If the board has paired, then the hole cards have missed the flop so returns missed
    """
    flop_values = list(card.value for card in flop_values)
    hole_card_values = list(card.value for card in hole_card_values)
    
    flop_values.sort()
    
    if any(card == flop_values[2] for card in hole_card_values):
        return 'top pair'
    elif any(card == flop_values[1] for card in hole_card_values):
         return 'middle pair'
    elif any(card == flop_values[0] for card in hole_card_values):
        return 'bottom pair'
    else:
        return 'missed'
    

def four_different_values_pocket_pair(hole_card_values, flop_values):
    """
    For pocket pairs that don't improve on the flop, this determines how many overcards 
    there are to the pocket pair
    """
    flop_values = list(card.value for card in flop_values)
    hole_card_values = list(card.value for card in hole_card_values)
    
    hole_card_number = hole_card_values[0]
    
    flop_values.sort()
    if hole_card_number > flop_values[2]:
        return 'overpair'
    elif hole_card_number > flop_values[1]:
        return 'pair with one overcard'
    elif hole_card_number > flop_values[0]:
        return 'pair with two overcards'
    else:
        return 'underpair'


def three_different_values(hand_values):
    """
    hands with three different values are two pair or three of a kind.
    """
    if any(hand_values.count(value)==3 for value in hand_values):
        return 'trips'
    else:
        return 'two pair'
    
def two_different_values():
    return 'full house or quads'


class Card(object):
    
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    def __str__(self):
        return "{},{}".format(self.value, self.suit)
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self,other_card):
        return self.suit == other_card.suit and self.value == other_card.value
    
    def __hash__(self):
        return hash(self.__repr__())
    
    
def generate_full_deck():

    full_deck = set()
    for value, suit in itertools.product(list(VALUES), list(SUITS)):
        full_deck.add(Card(value, suit))
    return full_deck

DECK = generate_full_deck()



class Cards(ABC):
    """
    For creating classes for groups of cards
    """
    def __init__(self, cards):
        assert len(cards) == self.EXPECTED_CARD_COUNT, "Wrong number of cards!"
        self.cards = cards

    def __repr__(self):
        ret = '<Cards:'
        for c in self.cards:
            ret += str(c) + ','
        ret += '>'
        return ret

    @property
    def values(self):
        return [c.value for c in self.cards]

    @property
    def suits(self):
        return [c.suit for c in self.cards]


class FlopCards(Cards):
    EXPECTED_CARD_COUNT = 3


class HoleCards(Cards):
    
    EXPECTED_CARD_COUNT = 2
    
    def analyse_flop(self, flop_cards):
        
        hand_values = flop_cards.values + self.values
        hand_suits = flop_cards.suits + self.suits

        functions = {5: partial(five_different_values, hand_values, hand_suits),
                     4: partial(four_different_values, self.values, flop_cards.values),
                     3: partial(three_different_values, hand_values),
                     2: two_different_values}
        
        func = len(set(hand_values))
        return functions[func]()

class PocketPair(Cards):
    EXPECTED_CARD_COUNT = 2

    def analyse_flop(self, flop_cards):
        
        hand_values = flop_cards.values + self.values

        functions = {4: partial(four_different_values_pocket_pair, self.values, flop_cards.values),
                     3: partial(three_different_values, hand_values),
                     2: two_different_values}
        
        func = len(set(hand_values))
        return functions[func]()




class HandType:
    
    """counts the number of flops that fit this hand type"""
    def __init__(self, name):
        self.name = name
        self.count = 0
        
    """returns the percentage chance of this hand type being flopped"""
    def percentage(self):
        percentage = self.count*100.0/19600.0 #there are 19600 possible flops hence dividing by 19600
        return percentage



def analyse(hole_cards):
    
    """
    creates a dictionary of all the different hand_types
    """
    hand_types_list = [
        'straight flush',
        'full house or quads',
        'flush',
        'straight',
        'trips',
        'two pair',
        'top pair',
        'middle pair',
        'bottom pair',
        'overpair',
        'pair with one overcard',
        'pair with two overcards',
        'underpair',
        'missed'
    ]

    types_dict = {}

    for item in hand_types_list:
        types_dict[item] = HandType(item)
    
    deck = generate_full_deck()
    deck.difference_update(c for c in hole_cards.cards) # Removes the selected hole cards from the flop

    
    for flop in itertools.combinations(deck,3):
        flop = FlopCards(list(flop))
        types_dict[hole_cards.analyse_flop(flop)].count += 1

    analysis_dict = {}
    for item in hand_types_list:
        percent = types_dict[item].percentage()
        if percent > 0:
            analysis_dict[item] = percent
    return analysis_dict
     


       
hc = HoleCards([Card(VALUES.ACE, SUITS.SPADES), Card(VALUES.SEVEN, SUITS.HEARTS)])

print(analyse(hc))