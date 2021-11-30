import time
from p2pnetwork.node import Node
from deck import Deck
from protocol import *
from tinyec import registry
import tinyec.ec as ec

class PlayerConnection (Node):

    # dictionary mapping connection IDs to Peer Names
    peers = {}
    curve = registry.get_curve('secp256r1')
    deck = Deck()
    shuffled_deck = deck
    secret = 1
    permutation = None

    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(PlayerConnection, self).__init__(host, port, id, callback, max_connections)

    def outbound_node_connected(self, connected_node):
        print(f"{self.id}: outbound_node_connected: {connected_node.id}")
        
    def inbound_node_connected(self, connected_node):
        print(f"{self.id}: inbound_node_connected: {connected_node.id}")

    def inbound_node_disconnected(self, connected_node):
        print(f"{self.id}: inbound_node_disconnected: {connected_node.id}")

    def outbound_node_disconnected(self, connected_node):
        print(f"{self.id}: outbound_node_disconnected: {connected_node.id}")

    def node_message(self, connected_node, data):

        # Handle all of the various message types
        msg_type = data['type']
        if msg_type == 'TEST':
            print(f"{self.id}: Received TEST msg from: {data['name']}")
            print(f"{data['content']}")
        elif msg_type == 'HELLO':
            print(f"{self.id}: Received HELLO msg from: {data['name']}")
            self.peers[connected_node.id] = data['name']
        elif msg_type == 'GOODBYE':
            print(f"{self.id}: Received GOODBYE msg from: {data['name']}")
            self.peers.pop(connected_node.id)
        elif msg_type == 'SETTINGS':
            # Sets up the parameters of the game (the curve to use plus any other options)
            print(f"{self.id}: Received SETTINGS msg from: {self.peers[connected_node.id]}")
            self.curve = registry.get_curve(data['curve'])
        elif msg_type == 'DECK_PREP':
            # Prepare deck between the currently connected nodes
            print(f"{self.id}: Received DECK_PREP msg from: {self.peers[connected_node.id]}")

            # Protocol 2 of Fast Mental Poker paper
            # Generate randomness and broadcast to other players
            card_prep_msg = []
            for i in range(0, 53):
                (g, gl, h, hl, r, t) = gen_rand_elem(self.curve)
                card_prep_msg.append([[g.x, g.y], [gl.x, gl.y], [h.x, h.y], [hl.x, hl.y], r, t])
                self.deck.prepare_card(hl, i)

            self.send_to_nodes({
                "type": "CARD_PREP",
                "cards": card_prep_msg
            })

        elif msg_type == 'CARD_PREP':
            print(f"{self.id}: Received CARD_PREP msg from: {self.peers[connected_node.id]}")

            for i in range(0, 53):
                # Parse the card prep message and verify the NIZK
                g = ec.Point(self.curve, data['cards'][i][0][0], data['cards'][i][0][1])
                gl = ec.Point(self.curve, data['cards'][i][1][0], data['cards'][i][1][1])
                h = ec.Point(self.curve, data['cards'][i][2][0], data['cards'][i][2][1])
                hl = ec.Point(self.curve, data['cards'][i][3][0], data['cards'][i][3][1])
                r = data['cards'][i][4]
                t = data['cards'][i][5]

                if not verify_nizk_dleq(g, gl, h, hl, r, t):
                    print(f"{self.id}: Detected cheating from: {self.peers[connected_node.id]}, I should quit.")
                else:
                    print(f"{self.id}: NIZK Verified... preparing card")
                    self.deck.prepare_card(hl, i)

        elif msg_type == 'START_SHUFFLE':
            print(f"{self.id}: Received START_SHUFFLE msg from: {self.peers[connected_node.id]}")
            (self.secret, self.permutation, self.shuffled_deck, m1) = gen_zka_shuffle_m1(self.deck)

        else:
            print(f"Received message of unknown type {msg_type} from node: {connected_node.id}")

        
    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")
