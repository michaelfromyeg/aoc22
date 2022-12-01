def part1():
    curr_max = float("-inf")

    with open("input.txt") as f:
        lines = f.readlines()
        calories = "\n".join(lines)

        groups = calories.split("\n\n\n")

        for group in groups:
            group_calories = group.split("\n")

            acc = 0
            for calorie in group_calories:
                if calorie.strip():
                    acc += int(calorie)
            curr_max = max(curr_max, acc)

    print(curr_max)


def part2():
    group_sums = []

    with open("input.txt") as f:
        lines = f.readlines()
        calories = "\n".join(lines)

        groups = calories.split("\n\n\n")

        for group in groups:
            group_calories = group.split("\n")

            acc = 0
            for calorie in group_calories:
                if calorie.strip():
                    acc += int(calorie)
            group_sums.append(acc)

    group_sums.sort(reverse=True)

    top_n_sum = 0
    n = 3
    for i in range(n):
        top_n_sum += group_sums[i]

    print(top_n_sum)


if __name__ == "__main__":
    part1()
    part2()
