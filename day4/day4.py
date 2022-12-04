def contains(a_s: int, a_e: int, b_s: int, b_e: int) -> bool:
    """
    For numeric pairs (a_s, a_e) and (b_s, b_e) where

    a_s <= a_e and,
    b_s <= b_e

    return whether either interval fully contain the other
    """
    return (a_s >= b_s and a_e <= b_e) or (b_s >= a_s and b_e <= a_e)


def overlaps(a_s: int, a_e: int, b_s: int, b_e: int) -> bool:
    """
    For numeric pairs (a_s, a_e) and (b_s, b_e) where

    a_s <= a_e and,
    b_s <= b_e

    return whether either interval overlaps at all
    """
    # b_s is inside a, or a_s is inside b
    return (a_s <= b_s and b_s <= a_e) or (b_s <= a_s and a_s <= b_e)


def part1():
    with open("input.txt") as f:
        lines = f.readlines()

        count = 0
        for line in lines:
            a, b = line.split(",")

            a_s, a_e = a.split("-")
            b_s, b_e = b.split("-")

            a_s, a_e, b_s, b_e = int(a_s), int(a_e), int(b_s), int(b_e)

            count = count + contains(a_s, a_e, b_s, b_e)
        print(count)


def part2():
    with open("input.txt") as f:
        lines = f.readlines()

        count = 0
        for line in lines:
            a, b = line.split(",")

            a_s, a_e = a.split("-")
            b_s, b_e = b.split("-")

            a_s, a_e, b_s, b_e = int(a_s), int(a_e), int(b_s), int(b_e)

            count = count + overlaps(a_s, a_e, b_s, b_e)
        print(count)


if __name__ == "__main__":
    part1()
    part2()
