# Elliptic Curve Points for representing cards

from tinyec import registry


class Deck:
    curve = registry.get_curve('secp256r1')
    cards = [None for _ in range(53)]

    def __init__(self):
        pass

    # Prepare the deck (Protocol 1: Fast Mental Poker)
    # 53 total points: base of deck + 52 cards
    # maps card values to group elements obtained from
    # Protocol 1 of Fast Mental Poker. Point is an EC point
    def prepare_card(self, point, idx):
        if self.cards[idx] is None:
            self.cards[idx] = point
        else:
            self.cards[idx] = self.cards[idx] + point
