import secrets
import hashlib

SHUFFLE_SECURITY_PARAM = 64

# Returns a non-interactive zero knowledge argument of knowledge
# for discrete logarithm equality (over an Elliptic Curve sub group)
# using the Fiat-Shamir Heuristic
def gen_nizk_dleq(curve, g, gx, h, hx, x):
    r = secrets.randbelow(curve.field.n)
    gr = g * r
    hr = h * r
    c = int(hashlib.sha256(f"{gr.x}{gr.y}{hr.x}{hr.y}{gx.x}{gx.y}{hx.x}{hx.y}".encode('utf-8')).hexdigest(), 16)
    t = r + c * x
    return (r, t)

def verify_nizk_dleq(g, gx, h, hx, r, t):
    hr = h * r
    gr = g * r
    c = int(hashlib.sha256(f"{gr.x}{gr.y}{hr.x}{hr.y}{gx.x}{gx.y}{hx.x}{hx.y}".encode('utf-8')).hexdigest(), 16)
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

    return (g, gx, h, hx, r, t)

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
def shuffle_cards(deck):

    shuffled_deck = deck

    permutation = [i for i in range(1,len(deck))]
    permutation = [0] + fisher_yates_shuffle(permutation)

    for i in range(0, len(deck)):
        x = secrets.randbelow(curve.field.n)
        shuffled_deck[i] = deck[permutation[i]] * x

    return (x, permutation, shuffled_deck)

# Applies the specified permutation 
# to the deck
def apply_shuffle(deck, shuffle):
    shuffled_deck = deck
    for i in range(0, len(deck)):
        shuffled_deck[i] = deck[shuffle[i]]


# Takes in two permutations of equal length and
# combines them into one e.g. \pi * \pi' 
def compose_shuffles(s1, s2):
    s = []
    for idx in s2:
        s.append(s1[idx])

    return s

# Protocol 4 of Fast Mental Poker: Shuffle Verification
# Prover's first set of messages to send to verifiers
# in interactive zero-knowledge argument protocol.
# Returns the secret and permutation used to create 
# the shuffled deck, along with a list of 3-tuples of the form
# (y, p, c) where the c's are the first messages sent in the ZKA
# protocol.
def gen_zka_shuffle_m1(deck):

    # Use Protocol 3 to shuffle the deck
    (x, p, shuffled_deck) = shuffle_cards(deck)

    m1 = []
    for i in range(0, SHUFFLE_SECURITY_PARAM):

        # Shuffle the deck again
        (y, p_prime, c) = shuffle_cards(shuffled_deck) 
        m1.append((y, p_prime, c))

    return (x, p, shuffled_deck, m1)

# Protocol 4 of Fast Mental Poker: Shuffle Verification
# Prover's second set of messages to send to verifiers
# in interactive zero-knowledge argument protocol.
# m1 param: 3-tuple of the form (y, p, c) where y is a secret,
#           p is a permutation, and c is the resulting deck
def gen_zka_shuffle_m2(shuffled_deck, x, p, m1, es):

    m2 = []
    for i in range(0, SHUFFLE_SECURITY_PARAM):

        if es[i] == 0:
            m2.append(m1[i])
        else:
            pp_prime = compose_shuffle(p, m1[i][1])
            m2.append((c, x * m1[i][0], pp_prime))

    return m2

# Protocol 4 of Fast Mental Poker for ZKA Shuffle Verification
# Takes in the pre-shuffled deck, the shuffled deck, and a message
# m2 that attests shuffled_deck is a valid shuffle of deck
def verify_zka_shuffle(deck, shuffled_deck, m2):

    for i in range(0, SHUFFLE_SECURITY_PARAM):
        c = m2[i][0]
        y = m2[i][1]
        p = m2[i][2] 

        ds = deck
        for j in range(0, len(deck)):
            ds[j] *= y

        ds = apply_shuffle(ds, p)

        for j in range(0, len(deck)):
            if ds[j] != c[j]:
                return False

    return True


# Protocol 2 of Fast Mental Poker paper
# Generate randomness and broadcast to other players
def send_deck_prep_points(curve):
    for i in range(0, 53):
        (g, gl, h, hl, r, t) = gen_rand_elem(curve)
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
        self.deck.prepare_card(hl, i)
