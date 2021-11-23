import time
from p2pnetwork.node import Node
from protocol import *
from tinyec import registry
import tinyec.ec as ec

class PlayerConnection (Node):

    # dictionary mapping connection IDs to Peer Names
    peers = {}
    curve = registry.get_curve('secp256r1')

    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(PlayerConnection, self).__init__(host, port, id, callback, max_connections)

    def outbound_node_connected(self, connected_node):
        print(f"outbound_node_connected: {connected_node.id}")
        
    def inbound_node_connected(self, connected_node):
        print(f"inbound_node_connected: {connected_node.id}")

    def inbound_node_disconnected(self, connected_node):
        print(f"inbound_node_disconnected: {connected_node.id}")

    def outbound_node_disconnected(self, connected_node):
        print(f"outbound_node_disconnected: {connected_node.id}")

    def node_message(self, connected_node, data):

        # Handle all of the various message types
        msg_type = data['type']
        if msg_type == 'HELLO':
            print(f"Received HELLO msg from: {data['name']}")
            self.peers[connected_node.id] = data['name']
        elif msg_type == 'GOODBYE':
            print(f"Received GOODBYE msg from: {data['name']}")
            self.peers.pop(connected_node.id)
        elif msg_type == 'SETTINGS':
            # Sets up the parameters of the game (the curve to use plus any other options)
            print(f"Received SETTINGS msg from: {self.peers[connected_node.id]}")
            self.curve = registry.get_curve(data['curve'])
        elif msg_type == 'DECK_PREP':
            # Prepare deck between the currently connected nodes
            print(f"Received DECK_PREP msg from: {self.peers[connected_node.id]}")

            # Protocol 2 of Fast Mental Poker paper
            # Generate randomness and broadcast to other players
            for i in range(0, 53):
                (g, gl, h, hl, r, t) = gen_rand_elem(self.curve)
                self.send_to_nodes({
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

        elif msg_type == 'CARD_PREP':
            print(f"Received CARD_PREP msg from: {self.peers[connected_node.id]}")
            # Parse the card prep message and verify the NIZK
            g = ec.Point(self.curve, data['gx'], data['gy'])
            gl = ec.Point(self.curve, data['glx'], data['gly'])
            h = ec.Point(self.curve, data['hx'], data['hy'])
            hl = ec.Point(self.curve, data['hlx'], data['hly'])
            r = data['r']
            t = data['t']
            if not verify_nizk_dleq(g, gl, h, hl, r, t):
                print(f"Detected cheating from: {self.peers[connected_node.id]}, I'm quitting.")
            else:
                print("NIZK Verified... preparing card")
                # TODO: Combine values from all players to finish deck preparation

        else:
            print(f"Received message of unknown type {msg_type} from node: {connected_node.id}")

        
    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")
