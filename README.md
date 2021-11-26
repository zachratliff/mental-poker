# mental-poker
CS227 Mental Poker Project

## Installation
python3 -m pip install -r requirements.txt

## Run
python3 poker.py


## TODO
- Set up group where DDH assumption holds :white_check_mark:
    - Using `sec256k1`, a prime-order elliptic curve E over the field GF(p), where p is prime and E has large embedding degree
- set up P2P message exchange between players :white_check_mark:
    - Using `p2pnetwork` python library for authenticated message exchange
- define various message types between players (e.g., hello, goodbye, keyexchange, etc.) 
- build fast mental poker protocols (1 - 6 in paper) 
    - Protocol 1 (Deck Preparation) :white_check_mark:
    - Protocol 2 (Generate a random element) :white_check_mark:
    - Protocol 3 (Shuffle)
    - Protocol 4 (Shuffle Verification)
    - Protocol 5 (Card Drawing)
    - Protocol 6 (Card Opening)

- study Fiat-Shamir heuristic and where we can use it within the Fast Mental Poker protocol
    - I think we can use it in Protocol 2 to generate a random element 
    - I'm not positive about whether or not we are able to use it in protocols 3 and 4 for shuffling. We should look into this. 
    - Using Fiat-Shamir will save us costs on player interaction / communication, but soundness of our NIZKs will only hold in the ROM

## TODO 2.0 (If time allows)
- Dockerize for demo
