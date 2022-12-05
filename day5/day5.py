from typing import List

STACK_WIDTH = 9
STACK_HEIGHT = 8


def part1():
    with open("input.txt") as f:
        # Create stacks to push and pop crates from
        stacks: List[List[str]] = []
        for i in range(STACK_WIDTH):
            stack = []
            stacks.append(stack)

        lines = f.readlines()

        for line in lines[0:STACK_HEIGHT]:
            line = line.strip()
            n = len(line)

            for i in range(0, n, 4):
                crate = line[i : i + 3].strip()
                if crate:
                    stacks[i // 4].insert(0, crate[1])

        for line in lines[STACK_HEIGHT + 2 :]:
            line = line.strip()

            n, from_to = line.split("from")
            s, e = from_to.split("to")

            n = n[5:].strip()
            n = int(n)

            s, e = s.strip(), e.strip()
            s, e = int(s), int(e)

            for i in range(n):
                if len(stacks[s - 1]) > 0:
                    last = stacks[s - 1].pop()
                    stacks[e - 1].append(last)

        retval = ""
        for stack in stacks:
            retval += stack[len(stack) - 1]
        print(retval)


def part2():
    with open("input.txt") as f:
        # Create stacks to push and pop crates from
        stacks: List[List[str]] = []
        for i in range(STACK_WIDTH):
            stack = []
            stacks.append(stack)

        lines = f.readlines()

        for line in lines[0:STACK_HEIGHT]:
            line = line.strip()
            n = len(line)

            for i in range(0, n, 4):
                crate = line[i : i + 3].strip()
                if crate:
                    stacks[i // 4].insert(0, crate[1])

        for line in lines[STACK_HEIGHT + 2 :]:
            line = line.strip()

            n, from_to = line.split("from")
            s, e = from_to.split("to")

            n = n[5:].strip()
            n = int(n)

            s, e = s.strip(), e.strip()
            s, e = int(s), int(e)

            for i in range(n):
                if len(stacks[s - 1]) > 0:
                    last = stacks[s - 1].pop()

                    # New bit: insert in the middle of the list each time
                    e_len = len(stacks[e - 1])
                    stacks[e - 1].insert(e_len - i, last)

        retval = ""
        for stack in stacks:
            retval += stack[len(stack) - 1]
        print(retval)


if __name__ == "__main__":
    part1()
    part2()
