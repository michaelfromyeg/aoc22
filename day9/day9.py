from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List

# It would be nice if the problem specified a needed grid size... pick huge values to accomodate
# TODO(michaelfromyeg): could the rope wrap around instead?
GRID_WIDTH = 1000
GRID_HEIGHT = 1000


class Direction(Enum):
    """
    A direction the head can move in the grid: up, down, left, or right.
    """

    U = 1
    D = 2
    L = 3
    R = 4


def opposite_direction(direction: Direction) -> Direction:
    """
    Get the opposite direction.
    """
    match direction:
        case Direction.U:
            return Direction.D
        case Direction.D:
            return Direction.U
        case Direction.R:
            return Direction.L
        case Direction.L:
            return Direction.R
    raise ValueError("Invalid direction %s given to opposite_direction", str(direction))


@dataclass
class Move:
    """
    A velocity-like move, with amount and direction.
    """

    d: Direction
    n: int


@dataclass
class Point:
    """
    Cartesian coordinates.
    """

    x: int
    y: int

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def adjacent(self, o: Point) -> bool:
        """
        Return if two points are adjacent in x, y (not diagonal).
        """
        same_col = self.y == o.y and abs(self.x - o.x) <= 1
        same_row = self.x == o.x and abs(self.y - o.y) <= 1
        diagonal = abs(self.x - o.x) <= 1 and abs(self.y - o.y) <= 1
        return same_col or same_row or diagonal

    def same_x_or_y(self, o: Point) -> bool:
        """
        True if points share x or y
        """
        return self.x == o.x or self.y == o.y


def str2direction(s: str) -> Direction:
    """
    Parse a string to a direction.
    """
    match s:
        case "U":
            return Direction.U
        case "D":
            return Direction.D
        case "L":
            return Direction.L
        case "R":
            return Direction.R
    raise ValueError("Move %s not recognized", s)


def build_grid(value: any) -> List[List[any]]:
    """
    Initialize the grid.
    """
    grid: List[List[any]] = []
    for _ in range(GRID_HEIGHT):
        row: List[any] = []
        for _ in range(GRID_WIDTH):
            row.append(value)
        grid.append(row)

    return grid


def move_point(direction: Direction, point: Point) -> Point:
    """
    Move point in direction. For now, assume input is always valid, i.e., never exceeds grid size.
    """
    match direction:
        case Direction.D:
            return Point(point.x, point.y + 1)
        case Direction.U:
            return Point(point.x, point.y - 1)
        case Direction.R:
            return Point(point.x + 1, point.y)
        case Direction.L:
            return Point(point.x - 1, point.y)
    raise ValueError("Invalid direction %s given to move_point", str(direction))


def draw_grid(
    grid: List[List[str]], head_position: Point, tail_position: Point
) -> None:
    """
    Debugging helper. Draw the grid with head and tail.
    """
    print(head_position, tail_position)
    for i, row in enumerate(grid):
        row_str = "".join(row)
        if i == tail_position.y:
            row_str = row_str[: tail_position.x] + "T" + row_str[tail_position.x + 1 :]
        if i == head_position.y:
            row_str = row_str[: head_position.x] + "H" + row_str[head_position.x + 1 :]

        print(row_str)
    print()


def draw_grid2(grid: List[List[str]], points: List[Point]) -> None:
    """
    Debugging helper. Draw the grid with head and tail.
    """
    for i, row in enumerate(grid):
        row_str = "".join(row)

        for j, point in enumerate(points):
            # Head point will always draw on top
            char = "H" if j == len(points) - 1 else str(j)
            if i == point.y:
                row_str = row_str[: point.x] + char + row_str[point.x + 1 :]

        print(row_str)
    print()


def process_move(
    direction: Direction,
    head_position: Point,
    tail_position: Point,
    grid: List[List[str]],
    t_visited_grid: List[List[bool]],
) -> None:
    """
    Process a move from the grid, updating t_visited_grid if need be.

    TODO: actually use grid, if need be. Just tracking points should be OK.
    """
    next_head_position = move_point(direction, head_position)
    next_tail_position = tail_position

    if next_head_position.adjacent(tail_position):
        # OK; leave tail where is for now
        pass
    elif next_head_position.same_x_or_y(tail_position):
        # Tail can simply follow the head in this case; will make adjacent
        next_tail_position = move_point(direction, tail_position)
    else:
        # We need to diagonally 'jump' the tail towards head; this is one way of doing that
        next_tail_position = move_point(
            opposite_direction(direction), next_head_position
        )

    t_visited_grid[next_tail_position.y][next_tail_position.x] = True
    # draw_grid(grid, next_head_position, next_tail_position)

    return next_head_position, next_tail_position


def process_move2(
    direction: Direction,
    points: List[Point],
    grid: List[List[str]],
    t_visited_grid: List[List[bool]],
) -> None:
    """
    Process a move from the grid, updating t_visited_grid if need be.

    Must now process n points, where the first element is the tail, and the last element is the head.
    """
    n_points = len(points)

    # Always move the head
    next_head = move_point(direction, points[n_points - 1])

    # print("process_move2")

    point_idx = n_points - 2
    for i in range(n_points - 2, -1, -1):
        # draw_grid2(grid, points)
        # print(next_head, next_mock_tail)
        next_mock_tail = points[i]

        if next_head == next_mock_tail or next_head.adjacent(next_mock_tail):
            # OK; leave tail where is for now
            pass
        elif next_head.same_x_or_y(next_mock_tail):
            # Tail can simply follow the head in this case; will make adjacent

            # This has to be more extensive for the many points case
            if next_head.x == next_mock_tail.x:
                dy = next_head.y - next_mock_tail.y
                if dy > 0:
                    next_mock_tail = move_point(Direction.D, next_mock_tail)
                else:
                    next_mock_tail = move_point(Direction.U, next_mock_tail)
            else:
                dx = next_head.x - next_mock_tail.x
                if dx > 0:
                    next_mock_tail = move_point(Direction.R, next_mock_tail)
                else:
                    next_mock_tail = move_point(Direction.L, next_mock_tail)
        else:
            # Jump diagonally up towards head; need work-around for hack-y trick

            # Question: where is there a gap?
            dy = next_head.y - next_mock_tail.y
            dx = next_head.x - next_mock_tail.x

            if abs(dy) > abs(dx):
                next_mock_tail = move_point(
                    Direction.U if dy > 0 else Direction.D, next_head
                )
            elif abs(dx) > abs(dy):
                next_mock_tail = move_point(
                    Direction.L if dx > 0 else Direction.R, next_head
                )
            else:
                next_mock_tail = move_point(
                    Direction.L if dx > 0 else Direction.R,
                    move_point(Direction.U if dy > 0 else Direction.D, next_head),
                )

        # # If mock_tail was the actual tail...
        if point_idx == 0:
            t_visited_grid[next_mock_tail.y][next_mock_tail.x] = True

        points[point_idx + 1] = next_head
        points[point_idx] = next_mock_tail

        next_head = next_mock_tail

        point_idx = point_idx - 1

    # draw_grid2(grid, points)
    return points


def part1() -> None:
    with open("input.txt") as f:
        lines = f.readlines()

        moves: List[Move] = []
        for line in lines:
            line = line.strip()
            d, n = line.split(" ")

            move = Move(d=str2direction(d), n=int(n))
            moves.append(move)

        grid = build_grid(".")
        t_visited_grid = build_grid(False)

        # Set the initial head_position to the (middle); tail starts overlapping
        head_position = Point(x=GRID_WIDTH // 2, y=GRID_HEIGHT // 2)
        tail_position = Point(x=GRID_WIDTH // 2, y=GRID_HEIGHT // 2)

        # Set the initial position for the head; tail has visited it by default!
        t_visited_grid[head_position.y][head_position.x] = True

        # draw_grid(grid, head_position, tail_position)

        # Process moves through the grid, updating head_position, tail_position throughout
        for move in moves:
            n = move.n
            while n > 0:
                head_position, tail_position = process_move(
                    move.d, head_position, tail_position, grid, t_visited_grid
                )
                n = n - 1

        total = 0
        for row in t_visited_grid:
            total += sum(row)

        # The answer!
        print(total)


def part2() -> None:
    with open("input.txt") as f:
        lines = f.readlines()

        moves: List[Move] = []
        for line in lines:
            line = line.strip()
            d, n = line.split(" ")

            move = Move(d=str2direction(d), n=int(n))
            moves.append(move)

        grid = build_grid(".")
        t_visited_grid = build_grid(False)

        # Set the initial head_position to the (middle); tail starts overlapping
        n_points = 10
        points: List[Point] = []
        for _ in range(n_points):
            points.append(Point(x=GRID_WIDTH // 2, y=GRID_HEIGHT // 2))

        # Set the initial position for the head; tail has visited it by default!
        head_position = points[n_points - 1]
        t_visited_grid[head_position.y][head_position.x] = True

        # print(points)
        # draw_grid2(grid, points)

        directions: List[Direction] = []
        for move in moves:
            for _ in range(move.n):
                directions.append(move.d)

        # Process moves through the grid, updating head_position, tail_position throughout
        for i, direction in enumerate(directions):
            points = process_move2(
                direction=direction,
                points=points,
                grid=grid,
                t_visited_grid=t_visited_grid,
            )

            # if i == 25:
            #     draw_grid2(grid, points)

        total = 0
        for row in t_visited_grid:
            total += sum(row)

        # The answer!
        print(total)


if __name__ == "__main__":
    part1()
    part2()
