from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple
from copy import deepcopy

DEBUG = True

INPUT_TEST_EXPECTED_BEFORE = """00 .......+....
01 ............
02 ............
03 ............
04 .....#...##.
05 .....#...#..
06 ...###...#..
07 .........#..
08 .........#..
09 .#########..
10 ............"""

INPUT_TEST_EXPECTED_AFTER = """.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########."""


@dataclass()
class Point:
    x: int
    y: int

    def cmove_down(
        self: Point, x_min: int, x_max: int, y_min: int, y_max: int, points: List[Point]
    ) -> bool:
        """
        Move the particle down if possible.
        """
        # if self.y + 1 > y_max:
        #     return False
        if Point(x=self.x, y=self.y + 1) in points:
            return False

        self.y = self.y + 1
        return True

    def cmove_down_left(
        self: Point, x_min: int, x_max: int, y_min: int, y_max: int, points: List[Point]
    ) -> bool:
        """
        Move the particle down and left if possible.
        """
        # if self.y + 1 > y_max:
        #     return False
        # if self.x - 1 < x_min:
        #     return False
        if Point(x=self.x - 1, y=self.y + 1) in points:
            return False

        self.x, self.y = self.x - 1, self.y + 1
        return True

    def cmove_down_right(
        self: Point, x_min: int, x_max: int, y_min: int, y_max: int, points: List[Point]
    ) -> bool:
        """
        Move the particle down and right if possible.
        """
        # if self.y + 1 > y_max:
        #     return False
        # if self.x + 1 > x_max:
        #     return False
        if Point(x=self.x + 1, y=self.y + 1) in points:
            return False

        self.x, self.y = self.x + 1, self.y + 1
        return True

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


# TODO(michaelfromyeg): use this data type...
@dataclass
class Sand:
    posn: Point
    at_rest: bool


ORIGIN = Point(x=500, y=0)
ORIGIN_S = "+"

AIR = "."
ROCK = "#"
SAND = "o"


def parse_point(point_str: str) -> Point:
    """
    Turn a x,y string into a point.
    """
    x, y = point_str.split(",")
    return Point(x=int(x), y=int(y))


def parse_rocks(line: str) -> List[Point]:
    """
    From a straight line polygon, given as

    a,b -> c,d -> e,f

    return a list of all x,y points covered.
    """
    expanded_points: List[Point] = []

    points_strs = line.split("->")
    n = len(points_strs)

    point: Optional[Point] = None
    next_point: Optional[Point] = None

    for i in range(0, n - 1):
        point = parse_point(points_strs[i].strip())
        next_point = parse_point(points_strs[i + 1].strip())

        if point.x == next_point.x:
            min_y, max_y = min(point.y, next_point.y), max(point.y, next_point.y)

            for y in range(min_y, max_y + 1):
                expanded_points.append(Point(x=point.x, y=y))
        else:  # the ys are equal
            min_x, max_x = min(point.x, next_point.x), max(point.x, next_point.x)

            for x in range(min_x, max_x + 1):
                expanded_points.append(Point(x=x, y=point.y))

    # TODO(michaelfromyeg): fix the code to not have duplicates
    return list(set(expanded_points))


def get_dimensions(rocks: List[Point]) -> Tuple[int, int, int, int]:
    """
    Determine visible portion of scan.
    """
    points = deepcopy(rocks)
    points.append(ORIGIN)

    xs = list(map(lambda points: points.x, points))
    ys = list(map(lambda points: points.y, points))

    x_min, x_max = min(*xs), max(*xs)
    y_min, y_max = min(*ys), max(*ys)

    return x_min - 1, x_max + 1, y_min, y_max + 1


def build_grid(
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
    rocks: List[Point],
    sand: List[Point],
) -> List[List[str]]:
    """
    Build a dx by dy grid (of air).
    """
    grid: List[List[str]] = []
    for y in range(y_min, y_max + 1):
        row: List[str] = []
        for x in range(x_min, x_max + 1):
            # TODO(michaelfromyeg): replace this with matrix check or similar; very slow
            if Point(x=x, y=y) in rocks:
                row.append(ROCK)
            elif Point(x=x, y=y) == ORIGIN:
                row.append(ORIGIN_S)
            elif Point(x=x, y=y) in sand:
                row.append(SAND)
            else:
                row.append(AIR)
        grid.append(row)
    return grid


def draw_grid(grid: List[List[str]]) -> str:
    """
    Draw a 2d-matrix to the terminal.
    """
    picture = ""
    for i, row in enumerate(grid):
        row.insert(0, f"{'0' + str(i) if i < 10 else str(i)} ")
        print("".join(row))
        picture += "".join(row) + "\n"

    # Add a blank line
    print()

    return picture[0 : len(picture) - 1]


def draw_rocks_and_sand(sand: List[Point], rocks: List[Point]) -> None:
    """
    Draw the rock grid, for debugging.
    """
    x_min, x_max, y_min, y_max = get_dimensions(rocks=rocks)

    grid = build_grid(
        x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, rocks=rocks, sand=sand
    )

    return draw_grid(grid)


def next_sand(sand: List[Point], rocks: List[Point]) -> int:
    """
    Try and move all sand, create a new piece of sand.

    If sand state is identical, remove sand.

    Modifies sand array.
    """
    x_min, x_max, y_min, y_max = get_dimensions(rocks=rocks)

    # First, create a new piece of sand, if it doesn't exist
    if ORIGIN not in sand:
        sand.append(Point(x=ORIGIN.x, y=ORIGIN.y))

    # Let's loop through sand in reverse order
    at_rest = 0
    for i in range(len(sand) - 1, -1, -1):
        particle = sand[i]

        all_points = deepcopy(rocks)
        all_points.extend(sand)

        try_down = particle.cmove_down(
            x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, points=all_points
        )
        if not try_down:
            try_down_left = particle.cmove_down_left(
                x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, points=all_points
            )
            if not try_down_left:
                try_down_right = particle.cmove_down_right(
                    x_min=x_min,
                    x_max=x_max,
                    y_min=y_min,
                    y_max=y_max,
                    points=all_points,
                )
                if not try_down_right:
                    at_rest = at_rest + 1

        sand[i] = particle

    return at_rest


def part1(filename: str) -> int:
    """
    Solve AoC Day 14 part 1.

    https://adventofcode.com/2022/day/14
    """
    rocks: List[Point] = []

    with open(filename) as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line:
                rocks.extend(parse_rocks(line))

    picture = draw_rocks_and_sand(sand=[], rocks=rocks)

    if DEBUG:
        assert picture == INPUT_TEST_EXPECTED_BEFORE

    s = []
    o = 0
    while True:
        n = next_sand(sand=s, rocks=rocks)

        draw_rocks_and_sand(sand=s, rocks=rocks)

        if o >= 24 and o == n:
            break
        else:
            o = n

    picture2 = draw_rocks_and_sand(sand=s, rocks=rocks)
    if DEBUG:
        assert picture2 == INPUT_TEST_EXPECTED_AFTER

    return len(s)


if __name__ == "__main__":
    retval = part1("input-test.txt" if DEBUG else "input.txt")

    if DEBUG:
        assert retval == 24
