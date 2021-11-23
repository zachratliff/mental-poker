# Elliptic Curve Points for representing cards

from tinyec import registry

class Deck:

    curve = registry.get_curve('secp256r1')
    cards = []
    # Prepare the deck (Protocol 1: Fast Mental Poker)
    # 53 total points: base of deck + 52 cards
    def __init__(self):
        ''' do nothing '''

