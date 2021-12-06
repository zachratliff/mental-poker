# Elliptic Curve Points for representing cards
import tinyec.ec as ec
from tinyec import registry

from poker_logic import ALL_CARDS


class Deck:
    curve = registry.get_curve('secp256r1')

    def __init__(self):
        self.cards = [None] * 53

    # Prepare the deck (Protocol 1: Fast Mental Poker)
    # 53 total points: base of deck + 52 cards
    # maps card values to group elements obtained from
    # Protocol 1 of Fast Mental Poker. Point is an EC point
    def prepare_card(self, point, idx):
        if self.cards[idx] is None:
            self.cards[idx] = point
        else:
            self.cards[idx] = self.cards[idx] + point

    # Given a list of (x,y) coords, set the deck up so 
    # that each card is an EC Point with coords (x,y)
    def setup_deck_from_xy_coords(self, point_list):
        for i in range(0, len(point_list)):
            self.cards[i] = ec.Point(self.curve, point_list[i][0], point_list[i][1])

    def to_point_list(self):
        point_list = []
        for card in self.cards:
            point_list.append([card.x, card.y])

        return point_list

    def get_mapping(self):
        return {(self.cards[i].x, self.cards[i].y): card for i, card in enumerate(ALL_CARDS, 1)}
