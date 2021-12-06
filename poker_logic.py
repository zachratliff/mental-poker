from collections import Counter
from dataclasses import dataclass, field
from enum import IntEnum, Enum, auto
from itertools import product
from operator import itemgetter
from typing import NamedTuple, Iterable, Optional, Set, Tuple, FrozenSet


class Rank(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Suit(Enum):
    CLUBS = auto()
    HEARTS = auto()
    DIAMONDS = auto()
    SPADES = auto()


class Card(NamedTuple):
    rank: Rank
    suit: Suit

    def __str__(self):
        return f'{self.rank.name.title()} of {self.suit.name.lower()}'


ALL_CARDS = [Card(rank, suit) for rank, suit in product(Rank, Suit)]


class HandRank(IntEnum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10


def flush_card_ranks(cards: Iterable[Card]) -> Optional[Set[Rank]]:
    """Given a set of cards, returns set of ranks of cards forming a flush if one exists and None otherwise"""
    suit_counts = Counter(card.suit for card in cards)
    suit, count = suit_counts.most_common(1)[0]
    if count >= 5:
        return {card.rank for card in cards if card.suit == suit}
    else:
        return None


STRAIGHTS = {**{5: {14, 2, 3, 4, 5}}, **{i: {i - j for j in range(5)} for i in range(6, 15)}}


def highest_straight(ranks: Iterable[Rank]) -> Optional[Rank]:
    """Returns the highest rank of straight if one exists and None otherwise"""
    rank_set = set(ranks)
    return max((Rank(highest_val) for highest_val, straight in STRAIGHTS.items() if straight.issubset(rank_set)),
               default=None)


def best_hand(cards: Iterable[Card]) -> Tuple[HandRank, Tuple, str]:
    """Returns the hand rank, tie-breaking tuple, and description of the best hand of given (seven) cards."""
    card_ranks = [card.rank for card in cards]

    rank_counts = Counter(card_ranks)
    sorted_counts = sorted(rank_counts.items(), key=itemgetter(1, 0), reverse=True)

    sorted_ranks = tuple(sorted(card_ranks, reverse=True))

    flush = flush_card_ranks(cards)

    if flush and (straight_val := highest_straight(flush)):
        if straight_val == 14:
            return HandRank.ROYAL_FLUSH, (), 'Royal flush'
        else:
            return HandRank.STRAIGHT_FLUSH, (straight_val,), f'{straight_val.name.title()}-high straight flush'
    elif sorted_counts[0][1] >= 4:
        four_of_a_kind_rank = sorted_counts[0][0]
        kicker = max(rank for rank in card_ranks if rank != four_of_a_kind_rank)
        return HandRank.FOUR_OF_A_KIND, (four_of_a_kind_rank, kicker), \
               f'Four {four_of_a_kind_rank.name.lower()}s with {kicker.name.lower()} kicker'
    elif sorted_counts[0][1] == 3 and sorted_counts[1][1] >= 2:
        three_of_a_kind = sorted_counts[0][0]
        two_of_a_kind = sorted_counts[1][0]
        return HandRank.FULL_HOUSE, (three_of_a_kind, two_of_a_kind), \
               f'{three_of_a_kind.name.title()}s full of {two_of_a_kind.name.lower()}s'
    elif flush:
        flush_ranks = tuple(sorted(flush, reverse=True))[:5]
        return HandRank.FLUSH, flush_ranks, f'Flush with ranks {", ".join(rank.name.lower() for rank in flush_ranks)}'
    elif straight_val := highest_straight(card_ranks):
        return HandRank.STRAIGHT, (straight_val,), f'{straight_val.name.title()}-high straight'
    elif sorted_counts[0][1] == 3:
        three_of_a_kind_rank = sorted_counts[0][0]
        kickers = tuple(rank for rank in sorted_ranks if rank != three_of_a_kind_rank)[:2]
        return HandRank.THREE_OF_A_KIND, (three_of_a_kind_rank,) + kickers, \
               f'Three {three_of_a_kind_rank.name.lower()}s with ' \
               f'{kickers[0].name.lower()} and {kickers[1].name.lower()} kickers'
    elif sorted_counts[1][1] == 2:
        higher_pair = sorted_counts[0][0]
        lower_pair = sorted_counts[1][0]
        kicker = max(rank for rank in card_ranks if rank != higher_pair and rank != lower_pair)
        return HandRank.TWO_PAIR, (higher_pair, lower_pair, kicker), \
               f'Pair of {higher_pair.name.lower()}s and pair of ' \
               f'{lower_pair.name.lower()}s with a {kicker.name.lower()} kicker'
    elif sorted_counts[0][1] == 2:
        pair_rank = sorted_counts[0][0]
        kickers = tuple(rank for rank in sorted_ranks if rank != pair_rank)[:3]
        return HandRank.PAIR, (pair_rank,) + kickers, \
               f'Pair of {pair_rank.name.lower()}s with kickers {", ".join(kicker.name.lower() for kicker in kickers)}'
    else:
        ranks = sorted_ranks[:5]
        return HandRank.HIGH_CARD, ranks, f'High card with ranks {", ".join(rank.name.lower() for rank in ranks)}'


@dataclass(order=True)
class Hand:
    hand_rank: int = field(compare=True)
    tie_breaking: Tuple = field(compare=True)
    cards: FrozenSet[Card] = field(compare=False)
    description: str = field(compare=False)

    def __init__(self, cards: Iterable[Card]):
        self.cards = frozenset(cards)
        self.hand_rank, self.tie_breaking, self.description = best_hand(self.cards)

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)
