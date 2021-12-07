# Mental Poker
CS227 Mental Poker Project: An implementation of the Fast Mental Poker protocol by Wei and Wang. 

## Installation
`python3 -m pip install -r requirements.txt`

We have tested using Python 3.8

## Run
`python3 poker.py`

The above program does the following:
 
1. performs the multi-party deck generation between two parties, Alice and Bob
2. performs the multi-party shuffle on the generated deck
3. Alice and Bob each draw 7 cards from the deck
4. Alice and Bob reveal their cards and the person with the best 5-card hand wins

## Implementation Details

- Using `sec256k1`, a prime-order elliptic curve E over the field GF(p), where p is prime and E has large embedding degree, and the DDH assumption is believed to hold
- set up P2P authenticated message exchange between players via the `p2pnetwork` python library
- Includes the core fast mental poker protocols (1 - 6 in paper) 
    - Protocol 1 (Deck Preparation) :white_check_mark:
    - Protocol 2 (Generate a random element) :white_check_mark:
    - Protocol 3 (Shuffle) :white_check_mark:
    - Protocol 4 (Shuffle Verification) :white_check_mark:
    - Protocol 5 (Card Drawing) :white_check_mark:
    - Protocol 6 (Card Opening) :white_check_mark:

