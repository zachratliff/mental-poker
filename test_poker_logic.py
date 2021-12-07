from poker_logic import Card, Rank, Suit, Hand

if __name__ == '__main__':
    c2 = Card(Rank.TWO, Suit.CLUBS)
    c3 = Card(Rank.THREE, Suit.CLUBS)
    c4 = Card(Rank.FOUR, Suit.CLUBS)
    c5 = Card(Rank.FIVE, Suit.CLUBS)
    c6 = Card(Rank.SIX, Suit.CLUBS)
    c7 = Card(Rank.SEVEN, Suit.CLUBS)
    c8 = Card(Rank.EIGHT, Suit.CLUBS)
    c9 = Card(Rank.NINE, Suit.CLUBS)
    ct = Card(Rank.TEN, Suit.CLUBS)
    cj = Card(Rank.JACK, Suit.CLUBS)
    cq = Card(Rank.QUEEN, Suit.CLUBS)
    ck = Card(Rank.KING, Suit.CLUBS)
    ca = Card(Rank.ACE, Suit.CLUBS)
    s2 = Card(Rank.TWO, Suit.SPADES)
    s3 = Card(Rank.THREE, Suit.SPADES)
    s4 = Card(Rank.FOUR, Suit.SPADES)
    s5 = Card(Rank.FIVE, Suit.SPADES)
    s6 = Card(Rank.SIX, Suit.SPADES)
    s7 = Card(Rank.SEVEN, Suit.SPADES)
    s8 = Card(Rank.EIGHT, Suit.SPADES)
    s9 = Card(Rank.NINE, Suit.SPADES)
    st = Card(Rank.TEN, Suit.SPADES)
    sj = Card(Rank.JACK, Suit.SPADES)
    sq = Card(Rank.QUEEN, Suit.SPADES)
    sk = Card(Rank.KING, Suit.SPADES)
    sa = Card(Rank.ACE, Suit.SPADES)
    d2 = Card(Rank.TWO, Suit.DIAMONDS)
    d3 = Card(Rank.THREE, Suit.DIAMONDS)
    d4 = Card(Rank.FOUR, Suit.DIAMONDS)
    d5 = Card(Rank.FIVE, Suit.DIAMONDS)
    d6 = Card(Rank.SIX, Suit.DIAMONDS)
    d7 = Card(Rank.SEVEN, Suit.DIAMONDS)
    d8 = Card(Rank.EIGHT, Suit.DIAMONDS)
    d9 = Card(Rank.NINE, Suit.DIAMONDS)
    dt = Card(Rank.TEN, Suit.DIAMONDS)
    dj = Card(Rank.JACK, Suit.DIAMONDS)
    dq = Card(Rank.QUEEN, Suit.DIAMONDS)
    dk = Card(Rank.KING, Suit.DIAMONDS)
    da = Card(Rank.ACE, Suit.DIAMONDS)
    h2 = Card(Rank.TWO, Suit.HEARTS)
    h3 = Card(Rank.THREE, Suit.HEARTS)
    h4 = Card(Rank.FOUR, Suit.HEARTS)
    h5 = Card(Rank.FIVE, Suit.HEARTS)
    h6 = Card(Rank.SIX, Suit.HEARTS)
    h7 = Card(Rank.SEVEN, Suit.HEARTS)
    h8 = Card(Rank.EIGHT, Suit.HEARTS)
    h9 = Card(Rank.NINE, Suit.HEARTS)
    ht = Card(Rank.TEN, Suit.HEARTS)
    hj = Card(Rank.JACK, Suit.HEARTS)
    hq = Card(Rank.QUEEN, Suit.HEARTS)
    hk = Card(Rank.KING, Suit.HEARTS)
    ha = Card(Rank.ACE, Suit.HEARTS)

    print(h7)
    print(sa)
    print(dq)

    royal_flush = Hand({sa, sk, sq, sj, st, s9, h2})
    other_royal_flush = Hand({ha, hk, hq, hj, ht, s3, c8})
    ten_straight_flush = Hand({ct, c9, c8, c7, c6, sa, sq})
    other_ten_straight_flush = Hand({ht, h9, h8, h7, h6, h5, h4})
    eight_straight_flush = Hand({d8, d7, d6, d5, d4, ca, ck})
    four_aces_with_king = Hand({da, ca, sa, ha, hk, ct, c5})
    four_aces_with_other_king = Hand({da, ca, sa, ha, hk, sk, ck})
    four_aces_with_queens = Hand({da, ca, sa, ha, hq, sq, cq})
    four_kings_with_aces = Hand({dk, ck, sk, hk, ha, sa, ca})
    tens_full_of_jacks = Hand({dt, ct, st, hj, sj, sa, ck})
    tens_full_of_jacks_different_kickers = Hand({dt, ct, st, hj, sj, s2, c2})
    tens_full_of_2s = Hand({dt, ct, st, c2, h2, d5, d7, d8})
    twos_full_of_aces = Hand({d2, c2, h2, da, ca, dt, d9})
    ace_king_flush = Hand({ha, hk, ht, h9, h8, c7, c6})
    ace_queen_flush = Hand({ha, hq, ht, h9, h8, c7, c6})
    ace_high_straight = Hand({ha, hk, sq, sj, ct, h9, h3})
    other_ace_high_straight = Hand({sa, dk, sq, sj, ct, ht, dt})
    king_high_straight = Hand({dk, sq, sj, ct, h9, d2, c2})
    three_threes = Hand({d3, s3, h3, h2, d6, st, sa})
    three_threes_equal_kickers = Hand({d3, s3, h3, h2, d4, st, sa})
    three_threes_worse_kickers = Hand({d3, s3, h3, h2, d4, st, sk})
    two_pair_aces_tens_nine = Hand({sa, ha, st, ht, d9, d3, d2})
    two_pair_actually_same = Hand({sa, ha, st, ht, d9, h9, d2})
    two_pair_also_same = Hand({st, ht, sa, ha, d9, h9, d2})
    two_pair_different = Hand({sa, ha, s4, h4, d9, h9, d2})
    pair_of_aces = Hand({sa, da, st, h9, d4, d3, h2})
    pair_of_tens = Hand({sa, dt, st, h9, d4, d3, h2})
    high_card = Hand({sa, sq, dt, s9, d5, d3, h2})

    print(royal_flush)
    print(other_royal_flush)
    print(ten_straight_flush)
    print(other_ten_straight_flush)
    print(eight_straight_flush)
    print(four_aces_with_king)
    print(four_aces_with_other_king)
    print(four_aces_with_queens)
    print(four_kings_with_aces)
    print(tens_full_of_jacks)
    print(tens_full_of_jacks_different_kickers)
    print(tens_full_of_2s)
    print(twos_full_of_aces)
    print(ace_king_flush)
    print(ace_queen_flush)
    print(ace_high_straight)
    print(other_ace_high_straight)
    print(king_high_straight)
    print(three_threes)
    print(three_threes_equal_kickers)
    print(three_threes_worse_kickers)
    print(two_pair_aces_tens_nine)
    print(two_pair_actually_same)
    print(two_pair_also_same)
    print(two_pair_different)
    print(pair_of_aces)
    print(pair_of_tens)
    print(high_card)

    assert royal_flush == \
           other_royal_flush > \
           ten_straight_flush == \
           other_ten_straight_flush > \
           eight_straight_flush > \
           four_aces_with_king == \
           four_aces_with_other_king > \
           four_aces_with_queens > \
           four_kings_with_aces > \
           tens_full_of_jacks == \
           tens_full_of_jacks_different_kickers > \
           tens_full_of_2s > \
           twos_full_of_aces > \
           ace_king_flush > \
           ace_queen_flush > \
           ace_high_straight == \
           other_ace_high_straight > \
           king_high_straight > three_threes == \
           three_threes_equal_kickers > \
           three_threes_worse_kickers > \
           two_pair_aces_tens_nine == \
           two_pair_actually_same == \
           two_pair_also_same > \
           two_pair_different > \
           pair_of_aces > \
           pair_of_tens > \
           high_card

    player_hands = {
        1: royal_flush,
        2: other_royal_flush,
        3: eight_straight_flush,
        4: ace_high_straight,
    }

    a_best_hand = max(player_hands.values())
    print(f'One best hand = {a_best_hand}')
    winning_players = [player for player, hand in player_hands.items() if hand == a_best_hand]
    print(f'Winning players = {winning_players}')
