from enum import Enum
from dataclasses import dataclass
from typing import Optional, List

CRT_W = 40
CRT_H = 6


class Command(Enum):
    NOOP = 0
    ADDX = 1


@dataclass
class Instruction:
    command: Command
    arg: Optional[int]

    def __str__(self) -> str:
        com = str(self.command)[8:].lower()
        arg = f" {self.arg}" if self.command == Command.ADDX else ""
        return f"{com}{arg}"


def str2command(s: str) -> Command:
    match s:
        case "noop":
            return Command.NOOP
        case "addx":
            return Command.ADDX
    raise ValueError(f"String {s} is not a command")


def n_cycles(command: Command) -> int:
    """
    Map a command to its number of cycles.
    """
    match command:
        case Command.NOOP:
            return 1
        case Command.ADDX:
            return 2
    raise ValueError(f"Command {command} is not a valid command")


def parse_command(values: List[str]) -> Instruction:
    """
    Parse a " "-separate string into an instruction.
    """
    command = str2command(values[0])
    match command:
        case Command.NOOP:
            return Instruction(command=command, arg=None)
        case Command.ADDX:
            return Instruction(command=command, arg=int(values[1]))
    raise ValueError(f"Command {command} is not a valid command")


def part1():
    # sum of signal strengths
    soss = 0

    cycle = 0
    x = 1

    instructions: List[Instruction] = []

    with open("input.txt") as f:
        lines = f.readlines()

        # print(lines)

        for line in lines:
            values = line.strip().split(" ")
            instructions.append(parse_command(values))

    drawing: List[List[str]] = []
    drawing_row: List[str] = []

    for instruction in instructions:
        for i in range(n_cycles(instruction.command)):
            # start of cycle, set cycle
            cycle = cycle + 1

            # during cycle, do draw (# or . and \n) and compute soss
            end = "\n" if cycle in [40, 80, 120, 160, 200, 240] else ""

            # print(
            #     str(instruction), "\t", cycle, cycle in [40, 80, 120, 160, 200, 240], x
            # )

            if (cycle - 1) % 40 in [x - 1, x, x + 1]:
                drawing_row.append("#")
            else:
                drawing_row.append(".")
            if end:
                drawing_row.append("\n")
                drawing.append(drawing_row)
                drawing_row = []

            # end of cycle, finish execution (a la writeback)
            if cycle in [20, 60, 100, 140, 180, 220]:
                soss += cycle * x

            if (
                instruction.command == Command.ADDX
                and i == n_cycles(instruction.command) - 1
            ):
                x += instruction.arg

    for drawing_row in drawing:
        print("".join(drawing_row), end="")

    print(f"\nsoss={soss}")


if __name__ == "__main__":
    part1()
