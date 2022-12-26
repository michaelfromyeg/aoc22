from dataclasses import dataclass
from typing import List

DEBUG = True

Composite = List[int] | int
Packet = List[Composite]


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


def is_balanced(pair: Pair) -> bool:
    """
    Determine if a pair of packets is ordered.
    """
    printf("is_balanced >> %s", pair)

    idx = 0

    while True:
        if type(pair.l[idx]) == int and type(pair.r[idx]) == int:
            printf("\tboth integers")
            li = pair.l[idx]
            ri = pair.r[idx]

            if li < ri:
                printf("\t\tl<r, true")
                return True
            elif ri < li:
                printf("\t\tr<l, false")
                return False

        idx = idx + 1

    return True


def part1() -> None:
    """ """

    pairs: List[Pair] = []

    with open("input-numbers.txt") as f:
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
        if is_balanced(pair):
            sum_indices = sum_indices + i

    print(sum_indices)


if __name__ == "__main__":
    part1()
