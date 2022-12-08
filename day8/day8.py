from __future__ import annotations
from typing import List


def build_grid(width: int, height: int) -> List[List[int]]:
    """
    Build a W x H matrix
    """
    grid = []
    for _ in range(height):
        row = []
        for _ in range(width):
            row.append(-1)
        grid.append(row)
    return grid


def is_visible(
    row: int, col: int, grid: List[List[int]], visible_grid: List[List[int]]
) -> bool:
    """
    Return whether the cell is visible

    TODO(michaelfromyeg): use assertions from the memoize values (need visible_from direction)
    """
    width = len(grid[0])
    height = len(grid)

    if row == 0 or col == 0 or row == width - 1 or col == height - 1:
        return True

    tree_height = grid[row][col]

    up = True
    for idx in range(row - 1, -1, -1):
        up = up and tree_height > grid[idx][col]

    down = True
    for idx in range(row + 1, height, 1):
        down = down and tree_height > grid[idx][col]

    left = True
    for idx in range(col - 1, -1, -1):
        left = left and tree_height > grid[row][idx]

    right = True
    for idx in range(col + 1, width, 1):
        right = right and tree_height > grid[row][idx]

    return up or down or left or right


def n_visible(grid: List[List[int]], visible_grid: List[List[int]]) -> int:
    """
    Return the visible trees in the grid
    """
    count = 0

    width = len(grid[0])
    height = len(grid)

    for row in range(height):
        for col in range(width):
            visible_grid[row][col] = is_visible(row, col, grid, visible_grid)
            if visible_grid[row][col]:
                count = count + 1
    return count


def get_score(row: int, col: int, grid: List[List[int]]) -> bool:
    """
    Return whether the cell is visible

    TODO(michaelfromyeg): again, speed this up with a bit of memoization (1 more than your neighbor...)
    """
    width = len(grid[0])
    height = len(grid)

    if row == 0 or col == 0 or row == width - 1 or col == height - 1:
        return 0

    tree_height = grid[row][col]

    up = 0
    for idx in range(row - 1, -1, -1):
        up += 1
        if tree_height <= grid[idx][col]:
            break

    down = 0
    for idx in range(row + 1, height, 1):
        down += 1
        if tree_height <= grid[idx][col]:
            break

    left = 0
    for idx in range(col - 1, -1, -1):
        left += 1
        if tree_height <= grid[row][idx]:
            break

    right = 0
    for idx in range(col + 1, width, 1):
        right += 1
        if tree_height <= grid[row][idx]:
            break

    return up * down * left * right


def max_score(grid: List[List[int]]) -> int:
    """
    Return the max scenic score in the grid
    """
    max_score = 0

    width = len(grid[0])
    height = len(grid)

    for row in range(height):
        for col in range(width):
            max_score = max(max_score, get_score(row, col, grid))

    return max_score


def partX() -> None:
    with open("input.txt") as f:
        lines = f.readlines()

        W = len(lines[0].strip())
        H = len(lines)

        grid = build_grid(W, H)

        # TODO(michaelfromyeg: use this structure; memoize the visible values
        visible_grid = build_grid(W, H)

        for row, line in enumerate(lines):
            line = line.strip()
            for column, char in enumerate(line):
                grid[row][column] = int(char)

        print(n_visible(grid=grid, visible_grid=visible_grid))
        print(max_score(grid=grid))


if __name__ == "__main__":
    partX()
