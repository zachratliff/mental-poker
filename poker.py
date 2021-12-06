import time

from deck import Deck
from player_connection import PlayerConnection
from poker_logic import Hand
from protocol import gen_rand_elem

HAND_SIZE = 7

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

card_mapping = alice.deck.get_mapping()

time.sleep(2)

alice.send_to_nodes({
    "type": "START_SHUFFLE",
})

time.sleep(30)

bob.send_to_nodes({
    "type": "START_SHUFFLE",
})

time.sleep(30)

# Draw cards from the deck and play poker. 7 cards each.
alice.send_to_nodes({
    "type": "DRAW_CARDS",
    "idxs": list(range(1, HAND_SIZE + 1))
})

bob.send_to_nodes({
    "type": "DRAW_CARDS",
    "idxs": list(range(HAND_SIZE + 1, 2 * HAND_SIZE + 1))
})

time.sleep(10)

alice_hand = Hand(card_mapping[alice.hand[i][0].x, alice.hand[i][0].y] for i in range(HAND_SIZE))
bob_hand = Hand(card_mapping[bob.hand[i][0].x, bob.hand[i][0].y] for i in range(HAND_SIZE))

print(f"Alice's hand: {alice_hand}")
print(f"Bob's hand: {bob_hand}")

# Reveal hands
alice.send_to_nodes({
    "type": "REQUEST_REVEAL"
})

bob.send_to_nodes({
    "type": "REQUEST_REVEAL"
})

time.sleep(20)

if alice_hand > bob_hand:
    print(f'Alice beats Bob with a hand of {alice_hand.description} over {bob_hand.description}.')
elif alice_hand < bob_hand:
    print(f'Bob beats Alice with a hand of {bob_hand.description} over {alice_hand.description}.')
else:
    print(f'Alice and Bob split the pot both with hands of {alice_hand.description}.')

time.sleep(10)

alice.stop()
bob.stop()
