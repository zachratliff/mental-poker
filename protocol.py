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
    c = int(hashlib.sha256((str(gr.x) + str(gr.y) + str(hr.x) + str(hr.y)).encode('utf-8')).hexdigest(), 16)
    t = r + c * x
    return (r, t)

def verify_nizk_dleq(g, gx, h, hx, r, t):
    hr = h * r
    gr = g * r
    c = int(hashlib.sha256((str(gr.x) + str(gr.y) + str(hr.x) + str(hr.y)).encode('utf-8')).hexdigest(), 16)
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
# We use Fiat-Shamir Heuristic to make the protocol
# non-interactive.
def gen_nizk_shuffle(deck):

    # Use Protocol 3 to shuffle the deck
    (x, p, deck) = shuffle_cards(deck)

    # Generate NIZK proof
    nizk = []
    for i in range(0, SHUFFLE_SECURITY_PARAM):

        # Shuffle the deck again
        (y, p_prime, c) = shuffle_cards(deck) 

        # Apply Fiat-Shamir Heuristic to non-interactively obtain a bit e
        # We should probably be smarter about how we generate e
        e = int(hashlib.sha256((str(c[i % len(deck)].x) + str(c[i % len(deck)].y)).encode('utf-8')).hexdigest(), 16) & 1

        if e == 0:
            nizk.append((c, y, p_prime))
        else:
            pp_prime = compose_shuffle(p, p_prime)
            nizk.append((c, x * y, pp_prime))

# Protocol 4 of Fast Mental Poker for NIZK Verification
def verify_nizk_shuffle(deck, shuffled_deck, nizk):

    for i in range(0, SHUFFLE_SECURITY_PARAM):
        c = nizk[i][0]
        y = nizk[i][1]
        p = nizk[i][2] 

        ds = deck
        for j in range(0, len(deck)):
            ds[j] *= y

        ds = apply_shuffle(ds, p)

        for j in range(0, len(deck)):
            if ds[j] != c[j]:
                return False

    return True

s1 = [0,4,5,3,2,1]
s2 = [0,3,2,4,5,1]
s3 = compose_shuffles(s1, s2)
print(s3)
