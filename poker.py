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
for i in range(0, 53):
    (g, gl, h, hl, r, t) = gen_rand_elem(alice.curve)
    alice.send_to_nodes({
                    "type": "CARD_PREP",
                    "card": i,
                    "gx": g.x,
                    "gy": g.y,
                    "glx": gl.x,
                    "gly": gl.y,
                    "hx": h.x,
                    "hy": h.y,
                    "hlx": hl.x,
                    "hly": hl.y,
                    "r": r,
                    "t": t
    })
    alice.deck.prepare_card(hl, i)

time.sleep(30)

for i in range(0, 53):
    if alice.deck.cards[i] != bob.deck.cards[i]:
        print("FAILURE")
    else:
        print(f"SUCCESSFULLY GENERATED CARD {i}")


alice.stop()
bob.stop()
