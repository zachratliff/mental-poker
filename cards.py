# Elliptic Curve Points for representing cards

from tinyec import registry

class Deck:

    cards = []
    curve = registry.get_curve('secp256r1')

    # Prepare the deck (Protocol 1: Fast Mental Poker)
    # 53 total points: base of deck + 52 cards
    def __init__(self):
        for k in range(1, 54):
            self.cards.append(k * curve.g)



