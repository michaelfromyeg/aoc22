from __future__ import annotations
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

DISK_SPACE = 70000000
NEEDED_SPACE = 30000000

# our system's file tree is composed of nodes, an abstract struct
# representing either a file or a directory, e.g., for

# - / (dir)
#   - i (file, size=100)
#   - a (dir)
#     - j (file, size=200)

# we would expect...

# Node("/", True, 300, [<ref 'i'>, <ref <'a'>])
# Node("/i", False, 100, [])
# Node("/a", True, 200, [<ref 'j'>])
# Node("/a/j", False, 200, [])


@dataclass
class Node:
    # the path to this node from the root; mostly for debugging help
    path: str
    # this file or folder's name (duplicated from path)
    name: str
    # true iff this is a directory
    dirent: bool
    # stores its own size;
    #   - if dir, size of all children / subdirs plus its files (-1 if unknown)
    #   - if file, file size
    size: int
    # this node's parent; optional for root only
    parent: Node
    # the files and folders in this node
    entries: List[Node]


### Data types to assist with parsing!


class Command(Enum):
    CD = 1
    LS = 2


@dataclass
class LsOutput:
    dirent: bool
    size: Optional[int]
    name: str


@dataclass
class Input:
    cmd: Command
    args: Optional[str]
    output: Optional[List[LsOutput]]


def parse_command(raw_command: str) -> Command:
    """
    Convert a string to an enum
    """
    match raw_command:
        case "ls":
            return Command.LS
        case "cd":
            return Command.CD
    raise ValueError(f"Unsupported command {raw_command} given to parse_command")


def parse_ls_output(raw_ls_output: str) -> LsOutput:
    """
    Convert line of ls output to class.
    """
    dir_or_size, name = raw_ls_output.split(" ")

    if dir_or_size == "dir":
        return LsOutput(dirent=True, size=None, name=name)
    return LsOutput(dirent=False, size=int(dir_or_size), name=name)


def parse_input(raw_input: str) -> Input:
    """
    Parse `Command` command from the command str; create input.
    """
    lines = raw_input.split("\n")
    first_line = lines[0].strip()

    values = first_line.split(" ")
    cmd = parse_command(values[0])

    args = None
    if cmd == Command.CD:
        args = values[1]

    output = None
    if cmd != Command.CD:
        # Remove the final blank line
        output_lines = lines[1 : len(lines) - 1]
        output = []
        for line in output_lines:
            output.append(parse_ls_output(line))

    return Input(cmd=cmd, args=args, output=output)


def build_path(old_path: str, name: str, dirent: bool) -> str:
    """
    String formatter helper for paths.
    """
    return f"{old_path}/{name}"


def process_command(command: Input, curr_node: Node) -> Node:
    """
    Process the command, returning an updated value for curr_node.
    """
    match command.cmd:
        case Command.LS:
            nodes = []

            for ls_output in command.output:
                # TODO: check if path already exists in curr_node.entries?
                path = build_path(curr_node.path, ls_output.name, ls_output.dirent)
                new_node = Node(
                    path=path,
                    name=ls_output.name,
                    dirent=ls_output.dirent,
                    size=-1 if ls_output.dirent else ls_output.size,
                    parent=curr_node,
                    entries=[] if ls_output.dirent else None,
                )
                nodes.append(new_node)

            curr_node.entries.extend(nodes)

            return curr_node

        case Command.CD:
            if command.args == "..":
                return curr_node.parent

            for entry in curr_node.entries:
                if command.args == entry.name:
                    return entry
            raise ValueError(f"Node with name {command.args} unknown by {curr_node}")

    raise ValueError(f"Command {command.cmd} not found")


def print_node_in_tree(node: Node, dir_size: bool) -> None:
    """
    As named
    """
    indent = "  " * node.path.count("/")
    details = (
        (f"dir, size={node.size}" if dir_size else "dir")
        if node.dirent
        else f"file, size={node.size}"
    )

    entry_str = f"{node.name} ({details})"

    print(f"{indent}- {entry_str}")


def print_tree(root_node: Node, dir_size: bool) -> None:
    """
    Walk and print the tree!
    """
    nodes = [root_node]
    while len(nodes) > 0:
        curr_node = nodes.pop()
        print_node_in_tree(curr_node, dir_size)
        if curr_node.entries:
            nodes.extend(curr_node.entries)


def compute_size(node: Node) -> None:
    if node.size != -1:
        return

    for entry in node.entries:
        compute_size(entry)

    total = 0
    for entry in node.entries:
        total += entry.size
    node.size = total


def sum_of_dirs_threshold(root_node: Node, threshold: int) -> int:
    total = 0

    nodes = [root_node]
    while len(nodes) > 0:
        curr_node = nodes.pop()

        if curr_node.dirent and curr_node.size <= threshold:
            total += curr_node.size

        if curr_node.entries:
            nodes.extend(curr_node.entries)

    return total


def size_of_dir_nearest(root_node: Node) -> int:
    """
    Return the size of the directory that is at least as big as target,
    and has the smallest gap above target.
    """

    def get_target(n: Node) -> int:
        """
        Find target for size_of_dir_nearest
        """
        return NEEDED_SPACE - (DISK_SPACE - n.size)

    target = get_target(root_node)
    size = float("inf")

    nodes = [root_node]
    while len(nodes) > 0:
        curr_node = nodes.pop()

        if (
            curr_node.dirent
            and curr_node.size >= target
            and (size - target) > (curr_node.size - target)
        ):
            size = curr_node.size

        if curr_node.entries:
            nodes.extend(curr_node.entries)

    return size


def partX():
    with open("input.txt") as f:
        lines = f.readlines()
        lines_str = "".join(lines)

        commands: List[Command] = []
        commands_str = lines_str.split("$")

        for command in commands_str:
            if command:
                commands.append(parse_input(command))

        # Path set to "" for correct indentation (everything above root)
        root_node = Node(
            path="", name="/", dirent=True, size=-1, parent=None, entries=[]
        )

        curr_node = root_node
        for command in commands[1:]:
            curr_node = process_command(command, curr_node)

        # print_tree(root_node=root_node, dir_size=False)

        compute_size(root_node)

        print_tree(root_node=root_node, dir_size=True)

        # part1
        print(sum_of_dirs_threshold(root_node=root_node, threshold=100000))

        # part 2
        print(size_of_dir_nearest(root_node=root_node))


if __name__ == "__main__":
    partX()
