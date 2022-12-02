def part1():
    """
    Compute rock-paper-scissors tournament total score.
    """

    score = 0
    with open("input.txt") as f:
        lines = f.readlines()

        for line in lines:
            opp, you = line.strip().split(" ")

            match f"{opp}{you}":
                case "AX":
                    score += 1 + 3
                case "BX":
                    score += 1 + 0
                case "CX":
                    score += 1 + 6
                case "AY":
                    score += 2 + 6
                case "BY":
                    score += 2 + 3
                case "CY":
                    score += 2 + 0
                case "AZ":
                    score += 3 + 0
                case "BZ":
                    score += 3 + 6
                case "CZ":
                    score += 3 + 3

    print(score)


def part2():
    """
    Compute rock-paper-scissors tournament total score.

    A = rock (1)
    B = paper (2)
    C = scissors (3)
    """

    score = 0
    with open("input.txt") as f:
        lines = f.readlines()

        for line in lines:
            opp, you = line.strip().split(" ")

            match f"{opp}{you}":
                case "AX":
                    score += 3 + 0
                case "BX":
                    score += 1 + 0
                case "CX":
                    score += 2 + 0
                case "AY":
                    score += 1 + 3
                case "BY":
                    score += 2 + 3
                case "CY":
                    score += 3 + 3
                case "AZ":
                    score += 2 + 6
                case "BZ":
                    score += 3 + 6
                case "CZ":
                    score += 1 + 6

    print(score)


if __name__ == "__main__":
    part1()
    part2()
