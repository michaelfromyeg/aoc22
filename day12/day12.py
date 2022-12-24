import copy
from typing import List, Tuple, Optional

from pprint import pprint

START = "S"
END = "E"


def value_of(c: str) -> int:
    match c:
        case "S":
            return ord("a")
        case "E":
            return ord("z")
        case _:
            return ord(c)


def is_valid_neighbour(
    grid: List[List[str]], u: Tuple[int, int], v: Tuple[int, int], mode: bool
) -> bool:
    """
    Check if v is a valid neighbour of u in grid.
    """
    u_x, u_y = u
    v_x, v_y = v

    if v_x < 0 or v_x >= len(grid[0]) or v_y < 0 or v_y >= len(grid):
        return False

    if mode:
        return value_of(grid[v_y][v_x]) + 1 >= value_of(grid[u_y][u_x])
    return value_of(grid[v_y][v_x]) <= value_of(grid[u_y][u_x]) + 1


def get_neighbours(
    grid: List[List[str]], u: Tuple[int, int], mode: bool
) -> List[Tuple[int, int]]:
    """
    Determine valid neighbours of n.
    """
    neighbours: List[Tuple[int, int]] = []

    u_x, u_y = u

    candidates = [(u_x - 1, u_y), (u_x + 1, u_y), (u_x, u_y + 1), (u_x, u_y - 1)]

    for v in candidates:
        if is_valid_neighbour(grid, u, v, mode):
            neighbours.append(v)

    return neighbours


def bfs(
    grid: List[List[str]],
    parent_grid: List[List[Tuple[int, int]]],
    distance_grid: List[List[float]],
    start: Tuple[int, int],
    end: Tuple[int, int],
    mode: bool,
) -> None:
    """
    Perform BFS on a list of nodes.
    """
    queue = [start]
    explored = [start]
    distance_grid[start[1]][start[0]] = 0

    while len(queue) > 0:
        u = queue.pop(0)

        for n in get_neighbours(grid, u, mode):
            if n not in explored:
                explored.append(n)
                parent_grid[n[1]][n[0]] = u
                distance_grid[n[1]][n[0]] = distance_grid[u[1]][u[0]] + 1
                queue.append(n)

                if n == end:
                    return None
    return None


def part1():
    grid: List[List[str]] = []
    parent_grid: List[List[Optional[Tuple[int, int]]]] = []
    distance_grid: List[List[float]] = []

    s: Tuple[int, int] = (-1, -1)
    t: Tuple[int, int] = (-1, -1)

    with open("input.txt") as f:
        lines = f.readlines()

        for y, row in enumerate(lines):
            row = row.strip()

            grid_row = []
            parent_grid_row = []
            distance_grid_row = []

            for x, c in enumerate(row):
                if c == START:
                    s = (x, y)
                if c == END:
                    t = (x, y)
                grid_row.append(c)
                parent_grid_row.append(None)
                distance_grid_row.append(float("inf"))

            grid.append(grid_row)
            parent_grid.append(parent_grid_row)
            distance_grid.append(distance_grid_row)

    # pprint(grid)

    bfs(
        grid=grid,
        parent_grid=parent_grid,
        distance_grid=distance_grid,
        start=s,
        end=t,
        mode=False,
    )

    # pprint(parent_grid)

    end = t
    count = 0
    while end != s:
        # print(f"{grid[end[1]][end[0]]}@{end} ->", end=" ")
        end = parent_grid[end[1]][end[0]]
        count = count + 1
    # print(f"{end}")

    print(count)


def part2():
    grid: List[List[str]] = []
    parent_grid: List[List[Optional[Tuple[int, int]]]] = []
    distance_grid: List[List[float]] = []

    ss: List[Tuple[int, int]] = []
    t: Tuple[int, int] = (-1, -1)

    with open("input.txt") as f:
        lines = f.readlines()

        for y, row in enumerate(lines):
            row = row.strip()

            grid_row = []
            parent_grid_row = []
            distance_grid_row = []

            for x, c in enumerate(row):
                if c == "a":
                    ss.append((x, y))
                if c == END:
                    t = (x, y)
                grid_row.append(c)
                parent_grid_row.append(None)
                distance_grid_row.append(float("inf"))

            grid.append(grid_row)
            parent_grid.append(parent_grid_row)
            distance_grid.append(distance_grid_row)

    # s = ss[0]

    bfs(
        grid=grid,
        parent_grid=parent_grid,
        distance_grid=distance_grid,
        start=t,
        end=(0, 0),
        mode=True,
    )

    # pprint(distance_grid)

    # could use ss instead
    mn = float("inf")
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == "a":
                mn = min(distance_grid[y][x], mn)
    print(mn)


if __name__ == "__main__":
    part1()  # 534; invert is_valid_neighbour check to see
    part2()  # 525
