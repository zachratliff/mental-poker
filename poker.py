import time
from player_connection import PlayerConnection
from deck import Deck
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

alice.send_to_nodes({
    "type": "TEST",
    "name": "alice",
    "content": [[alice.curve.g.x, alice.curve.g.y],[1,2,3]]
})

time.sleep(1)

alice.send_to_nodes({
    "type": "SETTINGS",
    "curve": "secp256r1",
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
    #alice.send_to_nodes({
    #                "type": "CARD_PREP",
    #                "card": i,
    #                "g": [g.x, g.y],
    #                "gl": [gl.x, gl.y],
    #                "h": [h.x, h.y],
    #                "hl": [hl.x, hl.y],
    #                "r": r,
    #                "t": t
    #})
    alice.deck.prepare_card(hl, i)

alice.send_to_nodes({
    "type": "CARD_PREP",
    "cards": card_prep_msg
})

time.sleep(30)

for i in range(0, 53):
    if alice.deck.cards[i] != bob.deck.cards[i]:
        print("FAILURE")
    else:
        print(f"SUCCESSFULLY GENERATED CARD {i}: ({alice.deck.cards[i].x},{alice.deck.cards[i].y})")


alice.stop()
bob.stop()
