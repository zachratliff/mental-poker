import secrets
import hashlib

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
# using Fisher-Yates shuffle
def fisher_yates_shuffle(s):
    for i in range(0, len(s) - 1):
        j = secrets.randbelow(len(s) - i)
        elem1 = s[i]
        elem2 = s[j + i]
        s[i] = elem2
        s[j + i] = elem1
        
    return s

