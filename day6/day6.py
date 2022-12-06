def partN(seq_n: int) -> None:
    """
    Print the Nth character in the string that completes a seq_n length sequence
    of non-repeating characters.
    """
    with open("input.txt") as f:
        line = f.readlines()[0]

        n = len(line)
        for i in range(0, n - seq_n):
            if len(set(line[i : i + seq_n])) == seq_n:
                print(i + seq_n)
                return  # no point in finding additional examples!


if __name__ == "__main__":
    partN(4)
    partN(14)
