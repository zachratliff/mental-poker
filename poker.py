import time
from player_connection import PlayerConnection
from deck import Deck

deck = Deck()

alice = PlayerConnection("127.0.0.1", 10001)
bob = PlayerConnection("127.0.0.1", 10002)

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

time.sleep(30)

alice.stop()
bob.stop()
