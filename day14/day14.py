from dataclasses import dataclass
from typing import Optional, List
from copy import deepcopy

DEBUG = True

INPUT_TEST_EXPECTED = """0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########."""


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class Sand:
    posn: Point
    at_rest: bool


ORIGIN = Point(x=500, y=0)
ORIGIN_S = "+"

AIR = "."
ROCK = "#"


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


def build_grid(
    x_min: int, x_max: int, y_min: int, y_max: int, rocks: List[Point]
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
        row.insert(0, f"{str(i)} ")
        print("".join(row))
        picture += "".join(row) + "\n"

    return picture[0 : len(picture) - 1]


def draw_rocks(rocks: List[Point]) -> None:
    """
    Draw the rock grid, for debugging.
    """
    points = deepcopy(rocks)
    points.append(ORIGIN)

    xs = list(map(lambda points: points.x, points))
    ys = list(map(lambda points: points.y, points))

    x_min, x_max = min(*xs), max(*xs)
    y_min, y_max = min(*ys), max(*ys)

    grid = build_grid(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, rocks=rocks)

    return draw_grid(grid)


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

    picture = draw_rocks(rocks)
    if DEBUG:
        assert picture == INPUT_TEST_EXPECTED

    return 0


if __name__ == "__main__":
    retval = part1("input-test.txt" if DEBUG else "input.txt")
    if DEBUG:
        assert retval == 24
