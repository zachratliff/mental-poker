import time
from player_connection import PlayerConnection

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

time.sleep(5) # Create here your main loop of the application

alice.stop()
bob.stop()
