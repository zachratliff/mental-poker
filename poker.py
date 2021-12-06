import time

from deck import Deck
from player_connection import PlayerConnection
from protocol import *

deck = Deck()

alice = PlayerConnection("127.0.0.1", 10001, id='alice')
bob = PlayerConnection("127.0.0.1", 10002, id='bob')

time.sleep(1)

alice.start()
bob.start()

time.sleep(1)

# Connect with Bob
alice.connect_with_node('127.0.0.1', 10002)

time.sleep(2)

# Send a dictionary message to Bob
alice.send_to_nodes({
    "type": "HELLO",
    "name": "alice"
})

bob.send_to_nodes({
    "type": "HELLO",
    "name": "bob"
})

time.sleep(1)

alice.send_to_nodes({
    "type": "DECK_PREP"
})

# Alice will send her own random elements
card_prep_msg = []
for i in range(0, 53):
    (g, gl, h, hl, r, t) = gen_rand_elem(alice.curve)
    card_prep_msg.append([[g.x, g.y], [gl.x, gl.y], [h.x, h.y], [hl.x, hl.y], r, t])
    alice.deck.prepare_card(hl, i)

alice.send_to_nodes({
    "type": "CARD_PREP",
    "cards": card_prep_msg
})

time.sleep(30)

for i in range(0, 53):
    if alice.deck.cards[i] != bob.deck.cards[i]:
        print(f"FAILURE VERIFYING NIZK FOR CARD {i}!!! WE SHOULD ABORT")
    else:
        print(f"SUCCESSFULLY GENERATED CARD {i}: ({alice.deck.cards[i].x},{alice.deck.cards[i].y})")
        #TODO: At this point we should map each elliptic curve point to a card value
        # Example:
        #  alice.deck.card[1] = ACE OF SPADES
        #  alice.deck.card[2] = TWO OF SPADES
        #  alice.deck.card[0] is reserved for the base of the deck and shouldn't be mapped

time.sleep(2)

alice.send_to_nodes({
    "type": "START_SHUFFLE",
})

time.sleep(30)

bob.send_to_nodes({
    "type": "START_SHUFFLE",
})

time.sleep(30)

# Draw cards from the deck and play poker
alice.send_to_nodes({
    "type": "DRAW_CARDS",
    "idxs": [1,2,3,4,5]
})

bob.send_to_nodes({
    "type": "DRAW_CARDS",
    "idxs": [6,7,8,9,10]
})

time.sleep(10)

# Reveal hands 
alice.send_to_nodes({
    "type": "REQUEST_REVEAL"
})

bob.send_to_nodes({
    "type": "REQUEST_REVEAL"
})

time.sleep(10)

# At this point Alice and Bob have both verified each other's 5-card hands
# and can check who won the 5-card draw
# TODO: Compare alice.hand with bob.hand and output winner
# To get each card in Alice and Bob's hand:
# alice Card i: alice.hand[i][0]
# bob Card i: bob.hand[i][0]
# where i = 0...4 (5 cards draw) 

# just apply mapping of these cards (elliptic curve points) to card values 
# and compare hands

time.sleep(10)

alice.stop()
bob.stop()
