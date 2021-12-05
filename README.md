# mental-poker
CS227 Mental Poker Project

## Installation
`python3 -m pip install -r requirements.txt`

## Run
`python3 poker.py`


## TODO
- Set up group where DDH assumption holds :white_check_mark:
    - Using `sec256k1`, a prime-order elliptic curve E over the field GF(p), where p is prime and E has large embedding degree
- set up P2P message exchange between players :white_check_mark:
    - Using `p2pnetwork` python library for authenticated message exchange
- define various message types between players (e.g., hello, goodbye, keyexchange, etc.) 
- build fast mental poker protocols (1 - 6 in paper) 
    - Protocol 1 (Deck Preparation) :white_check_mark:
    - Protocol 2 (Generate a random element) :white_check_mark:
    - Protocol 3 (Shuffle) :white_check_mark:
    - Protocol 4 (Shuffle Verification) :white_check_mark:
    - Protocol 5 (Card Drawing) (in progress)
    - Protocol 6 (Card Opening) (in progress)

- Develop actual card game
    - Something like War is the simplest
    - Would be more interesting to do Blackjack between two parties (a dealer and player)
    - Texas Hold'em is a stretch goal, since that involves us creating quite a bit of poker logic

- study Fiat-Shamir heuristic and where we can use it within the Fast Mental Poker protocol
    - I think we can use it in Protocol 2 to generate a random element :white_check_mark:
    - Using Fiat-Shamir will save us costs on player interaction / communication, but soundness of our NIZKs will only hold in the ROM

## TODO 2.0 (If time allows)
- Dockerize for demo
