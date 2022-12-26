from dataclasses import dataclass
from typing import List
from functools import cmp_to_key
from copy import deepcopy

from pprint import pprint

DEBUG = True

# Note: these types are wrong; they need to depend on
#       self-reference but can't, even with `from __future__ import annotations`

Composite = List[int] | int
Packet = List[Composite] | Composite


def is_int(c: Composite) -> bool:
    """
    Determine if composite type is a list.
    """
    return type(c) == int


def is_list(c: Composite) -> bool:
    """
    Determine if composite type is a list.
    """
    return type(c) == list


def bool_to_cmp(b: bool | None) -> int:
    """
    Convert a boolean value to a cmp-friendly one.
    """
    if b is None:
        return 0
    elif b is False:
        return 1
    else:  # b is True
        return -1


def printf(message, *args):
    """
    A replacement for my favorite C debugging macro.
    """
    if DEBUG:
        print(f"DEBUG: {message % args}")


@dataclass
class Pair:
    """
    A left (l) and right (r) packet.
    """

    l: Packet
    r: Packet


def parse_packet(src: str, start: int, cease: int) -> Packet:
    """
    Turn a nested list-like, e.g., [1, 2, [3, 4], 5], into an actual list.
    """
    packet: Packet = []

    printf(
        "parse_packet >> src=%s, start=%d, cease=%d, src[start:cease]=%s",
        src,
        start,
        cease,
        src[start:cease],
    )

    # Handle empty list case
    if start + 1 == cease - 1:
        printf("\tempty")
        return packet

    s = start

    while s < cease:
        if src[s + 1 : s + 2] == "[":
            printf("\tnested")

            # Find the next balanced paranthesis... in a hack-y way (I'm sure there is better)

            # (initialize c, our closing paren and score, posve for number of new open parens found)
            c = s + 1
            score = -1

            # (exit condition: next character is ] and score is 0)
            while (src[c : c + 1] != "]" or score != 0) and c <= cease:
                # Shift the "score" around
                if src[c : c + 1] == "[":
                    score = score + 1
                elif src[c : c + 1] == "]":
                    score = score - 1
                c = c + 1

            nested_packet = parse_packet(src, s + 1, c + 1)
            packet.append(nested_packet)
            s = c + 1
        elif str.isdigit(src[s + 1 : s + 3]):
            printf("\ttwo-digit")

            packet.append(int(src[s + 1 : s + 3]))
            s = s + 2
        elif str.isdigit(src[s + 1 : s + 2]):
            printf("\tone-digit")

            packet.append(int(src[s + 1 : s + 2]))
            s = s + 1
        else:
            # print("\tnothing (comma?)")
            s = s + 1

    return packet


def is_balanced(pair: Pair) -> bool | None:
    """
    Determine if a pair of packets is ordered.
    """
    printf("is_balanced >> %s", pair)

    idx = 0

    if len(pair.l) == 0 and len(pair.r) == 0:
        return None

    if len(pair.l) == 0:
        return True

    if len(pair.r) == 0:
        return False

    while idx < len(pair.l):
        if idx >= len(pair.r):
            return False

        if is_int(pair.l[idx]) and is_int(pair.r[idx]):
            printf("\tboth integers")
            li = pair.l[idx]
            ri = pair.r[idx]

            if li < ri:
                printf("\t\tl<r, true")
                return True
            elif ri < li:
                printf("\t\tr<l, false")
                return False

        elif is_list(pair.l[idx]) and is_list(pair.r[idx]):
            printf("\tboth lists")

            sub_pair = Pair(l=pair.l[idx], r=pair.r[idx])

            retval = is_balanced(sub_pair)
            if retval is not None:
                return retval

        elif is_int(pair.l[idx]):
            printf("\tleft is int")

            copy_pair = deepcopy(pair)

            copy_pair.l[idx] = [copy_pair.l[idx]]

            retval = is_balanced(copy_pair)
            if retval is not None:
                return retval

        elif is_int(pair.r[idx]):
            printf("\tright is int")

            copy_pair = deepcopy(pair)

            copy_pair.r[idx] = [copy_pair.r[idx]]

            retval = is_balanced(copy_pair)
            if retval is not None:
                return retval

        else:
            printf("\tmissed every case?")

            return None

        idx = idx + 1

    if idx < len(pair.r):
        return True

    return None


def part1(filename: str) -> None:
    """
    Part 1 of AoC day 13.

    https://adventofcode.com/2022/day/13#part1
    """

    pairs: List[Pair] = []

    with open(filename) as f:
        chunk = f.read()
        groups = chunk.split("\n\n")

        for group in groups:
            l, r = group.split("\n")
            pair = Pair(
                l=parse_packet(l, 0, len(l)),
                r=parse_packet(r, 0, len(r)),
            )
            pairs.append(pair)

    for pair in pairs:
        printf("pair=%s", pair)

    sum_indices = 0
    for i, pair in enumerate(pairs):
        retval = is_balanced(pair)

        if retval is False:
            printf("\tretval=false")
        elif retval is None:
            printf("\tretval=None, equal lists")
        else:  # if retval is True
            printf("\tretval=true")
            sum_indices = sum_indices + (i + 1)
            printf("\tsum_indices=%d", sum_indices)

    return sum_indices


def part2(filename: str) -> None:
    """
    Part 2 of AoC day 13.

    https://adventofcode.com/2022/day/13#part2
    """

    packets: List[Pair] = []

    with open(filename) as f:
        chunk = f.read()
        groups = chunk.split("\n\n")

        for group in groups:
            l, r = group.split("\n")

            packets.append(parse_packet(l, 0, len(l)))
            packets.append(parse_packet(r, 0, len(r)))

    for packet in packets:
        printf("packet=%s", packet)

    DIVIDER_A = [[2]]
    DIVIDER_B = [[6]]

    packets.append(DIVIDER_A)
    packets.append(DIVIDER_B)

    sorted_p = list(
        sorted(
            packets,
            key=cmp_to_key(lambda l, r: bool_to_cmp(is_balanced(Pair(l=l, r=r)))),
        )
    )

    return (sorted_p.index(DIVIDER_A) + 1) * (sorted_p.index(DIVIDER_B) + 1)


if __name__ == "__main__":
    # case1_1 = part1("input.txt")
    # print(f"case1_1={case1_1}")

    case2_1 = part2("input.txt")
    print(f"case2_1={case2_1}")
