from typing import List


def priority(c: str) -> int:
    """
    Return the priority of a letter. Assumes c is a single-character in [a-zA-Z].
    """
    if ord(c) >= 65 and ord(c) <= 90:
        return ord(c) - 38
    return ord(c) - 96


assert priority("a") == 1
assert priority("b") == 2
assert priority("z") == 26
assert priority("A") == 27
assert priority("B") == 28
assert priority("Z") == 52


def common_letter(a: str, b: str) -> str:
    """
    Find the common letter c between two strings. Assume such a letter exists; and that a and b are the same length.
    """
    assert len(a) == len(b)

    for c in a:
        if c in b:
            return c

    raise ValueError("strings %s and %s don't have a common string", a, b)


def common_letter2(a: str, b: str, c: str) -> str:
    """
    Find the common letter c between three strings. Assume such a letter exists.
    """
    for char in a:
        if char in b and char in c:
            return char

    raise ValueError("strings %s, %s and %s don't have a common string", a, b, c)


assert common_letter("a", "a") == "a"
assert common_letter("ba", "ca") == "a"
assert common_letter("ca", "ba") == "a"
assert common_letter("bbbbbbabbbb", "ccacccccccc") == "a"


def make_groups(l: List[str]) -> List[str]:
    """
    Divide list into groups of 3
    """
    for i in range(0, len(l), 3):
        yield l[i : i + 3]


def part1():
    total = 0
    with open("input.txt") as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip()
            n = len(line)
            if n % 2 != 0:
                raise ValueError("line length not even %s", line)

            a, b = line[: n // 2], line[n // 2 :]
            total += priority(common_letter(a, b))
    print(total)


def part2():
    total = 0
    with open("input.txt") as f:
        lines = f.readlines()
        groups = make_groups(lines)

        for a, b, c in groups:
            total += priority(common_letter2(a, b, c))
    print(total)


if __name__ == "__main__":
    part1()
    part2()
