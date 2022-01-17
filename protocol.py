import hashlib
import hmac
import secrets

from deck import Deck

SHUFFLE_SECURITY_PARAM = 5
HMAC_KEY = b'fd9499da3f13872eedc128019aa8cb484cd5ed8f2526e05579b99689f61ecb1b'

# Returns a non-interactive zero knowledge argument of knowledge
# for discrete logarithm equality (over an Elliptic Curve sub group)
# using the Fiat-Shamir Heuristic
def gen_nizk_dleq(curve, g, gx, h, hx, x):
    r = secrets.randbelow(curve.field.n)
    gr = g * r
    hr = h * r
    c = int(hmac.new(HMAC_KEY, f"{gr.x}{gr.y}{hr.x}{hr.y}{gx.x}{gx.y}{hx.x}{hx.y}".encode('utf-8'), hashlib.sha256).hexdigest(), 16)
    t = r + c * x
    return r, t


def verify_nizk_dleq(g, gx, h, hx, r, t):
    hr = h * r
    gr = g * r
    c = int(hmac.new(HMAC_KEY, f"{gr.x}{gr.y}{hr.x}{hr.y}{gx.x}{gx.y}{hx.x}{hx.y}".encode('utf-8'), hashlib.sha256).hexdigest(), 16)
    gt = g * t
    ht = h * t

    gxc = gx * c
    hxc = hx * c

    return (gt == gr + gxc) and (ht == hr + hxc)


# This function generates a random element for the deck preparation
# protocol. A ZKA of Discrete Logarithm Equality is provided. Additionally,
# we use the Fiat-Shamir Heuristic to make the ZKA protocol non-interactive. 
def gen_rand_elem(curve):
    g = secrets.randbelow(curve.field.n) * curve.g
    h = secrets.randbelow(curve.field.n) * curve.g
    x = secrets.randbelow(curve.field.n)
    gx = g * x
    hx = h * x

    (r, t) = gen_nizk_dleq(curve, g, gx, h, hx, x)

    return g, gx, h, hx, r, t


# Unbiased permutation generation
# using Fisher-Yates shuffle.
def fisher_yates_shuffle(s):
    for i in range(0, len(s) - 1):
        j = secrets.randbelow(len(s) - i)
        elem1 = s[i]
        elem2 = s[j + i]
        s[i] = elem2
        s[j + i] = elem1

    return s


# Protocol 3 of Fast Mental Poker: Shuffle the Deck
# Returns a shuffled deck
def shuffle_cards(deck):
    shuffled_deck = Deck()

    permutation = list(range(1, len(deck.cards)))
    permutation = [0] + fisher_yates_shuffle(permutation)
    x = secrets.randbelow(deck.curve.field.n)

    for i in range(0, len(deck.cards)):
        shuffled_deck.cards[i] = deck.cards[permutation[i]] * x

    return x, permutation, shuffled_deck


# Applies the specified permutation
# to the deck
def apply_shuffle(deck, shuffle):
    shuffled_deck = Deck()
    for i in range(0, len(deck.cards)):
        shuffled_deck.cards[i] = deck.cards[shuffle[i]]

    return shuffled_deck


# Takes in two permutations of equal length and
# combines them into one e.g. \pi * \pi' 
def compose_shuffles(s1, s2):
    s = []
    for idx in s2:
        s.append(s1[idx])

    return s


# Protocol 4 of Fast Mental Poker: Shuffle Verification
# Uses Fiat-Shamir heuristic to make protocol non-interactive
# Returns the secret and permutation used to create 
# the shuffled deck, along with a list of 3-tuples of the form
# (y, p, c) where the c's are the first messages sent in the ZKA
# protocol.
def gen_nizk_shuffle(deck):
    # Use Protocol 3 to shuffle the deck
    (x, p, shuffled_deck) = shuffle_cards(deck)

    m = []
    for i in range(0, SHUFFLE_SECURITY_PARAM):
        # Shuffle the deck again
        (y, p_prime, c) = shuffle_cards(shuffled_deck)

        # Generate es
        rom_query = ""
        for z in deck.cards:
            rom_query += f"{z.x}{z.y}"

        for z in shuffled_deck.cards:
            rom_query += f"{z.x}{z.y}"

        for z in c.cards:
            rom_query += f"{z.x}{z.y}"

        e = int(hmac.new(HMAC_KEY, rom_query.encode('utf-8'), hashlib.sha256).hexdigest(), 16) & 1

        if e == 0:
            m.append((c, y, p_prime))
        else:
            pp_prime = compose_shuffles(p, p_prime)
            m.append((c, x * y, pp_prime))

    return x, p, shuffled_deck, m


# Protocol 4 of Fast Mental Poker for ZKA Shuffle Verification
# Takes in the pre-shuffled deck, the shuffled deck, and a message
# m that attests shuffled_deck is a valid shuffle of deck.
# Uses Fiat-Shamir Heuristic
def verify_nizk_shuffle(deck, shuffled_deck, m):
    for i in range(0, SHUFFLE_SECURITY_PARAM):
        c = m[i][0]
        y = m[i][1]
        p = m[i][2]

        # Generate es
        rom_query = ""

        for z in deck.cards:
            rom_query += f"{z.x}{z.y}"

        for z in shuffled_deck.cards:
            rom_query += f"{z.x}{z.y}"

        for z in c.cards:
            rom_query += f"{z.x}{z.y}"

        e = int(hmac.new(HMAC_KEY, rom_query.encode('utf-8'), hashlib.sha256).hexdigest(), 16) & 1

        ds = Deck()
        for j in range(0, len(deck.cards)):
            if e == 0:
                ds.cards[j] = shuffled_deck.cards[j] * y
            else:
                ds.cards[j] = deck.cards[j] * y

        ds = apply_shuffle(ds, p)

        for j in range(0, len(deck.cards)):
            if ds.cards[j] != c.cards[j]:
                return False

    return True
