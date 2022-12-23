from enum import Enum
from dataclasses import dataclass
from typing import List, Literal, Tuple

ROUNDS = 20


def div_by_3(x: int) -> int:
    return x // 3


class Operation(Enum):
    ADD = "+"
    MUL = "*"


def str_expression(s: Literal["old"] | int) -> str:
    if type(s) == int:
        return str(s)

    return str(s)[16:19]


@dataclass
class Expression:
    a: Literal["old"] | int
    b: Literal["old"] | int
    op: Operation

    def __str__(self) -> str:
        return f"{str_expression(self.a)} {self.op.value} {str_expression(self.b)}"


@dataclass
class Test:
    by: int
    yay_target: int
    nay_target: int

    def __str__(self) -> str:
        return f"{self.yay_target} if x / {self.by} == 0 else {self.nay_target}"


@dataclass
class Monkey:
    _id: int
    starting_items: List[int]
    expression: Expression
    test: Test

    def __str__(self) -> str:
        return f"""_id={self._id}
starting_items={self.starting_items}
expression={self.expression}
test={self.test}
        """


def parse_starting_items(s: str) -> List[int]:
    _, items = s.split(":")
    items = items.strip()
    items = items.split(", ")
    return list(map(lambda i: int(i), items))


def parse_old_or_int(s: str) -> Literal["old"] | int:
    return Literal["old"] if s == "old" else int(s)


def parse_expression(s: str) -> Expression:
    _, expr = s.split(":")
    expr = expr.strip()

    if "*" in expr:
        op = Operation.MUL

        a, b = expr.split("*")
        a = a.strip()[6:]
        b = b.strip()
        return Expression(a=parse_old_or_int(a), b=parse_old_or_int(b), op=op)

    if "+" in expr:
        op = Operation.ADD

        a, b = expr.split("+")
        a = a.strip()[6:]
        b = b.strip()
        return Expression(a=parse_old_or_int(a), b=parse_old_or_int(b), op=op)

    raise ValueError(f"No symbol found in expr {s}")


def parse_test(lines: List[str]) -> Test:
    by_tokens = lines[0].split(" ")
    by = int(by_tokens[len(by_tokens) - 1])

    yay_target = int(lines[1][-1])
    nay_target = int(lines[2][-1])

    return Test(by=by, yay_target=yay_target, nay_target=nay_target)


def parse_monkey(monkey_str: str) -> Monkey:
    parts = monkey_str.split("\n")

    _id = int(parts[0][-2])  # only works for monkeys with ID 0-9
    starting_items = parse_starting_items(parts[1])
    expression = parse_expression(parts[2])
    test = parse_test(parts[3:6])

    return Monkey(
        _id=_id, starting_items=starting_items, expression=expression, test=test
    )


def do_expression(expression: Expression, n: int) -> int:
    def parse_old(arg: Literal["old"] | int) -> int:
        return n if arg == Literal["old"] else arg

    match expression.op:
        case Operation.ADD:
            return parse_old(expression.a) + parse_old(expression.b)
        case Operation.MUL:
            return parse_old(expression.a) * parse_old(expression.b)

    raise ValueError(f"Invalid expression operation {expression.op}")


def do_test(test: Test, n: int) -> int:
    return test.yay_target if n % test.by == 0 else test.nay_target


def pass_item(monkey: Monkey, new_item: int, monkeys: List[Monkey]) -> None:
    index = do_test(monkey.test, new_item)

    target_monkey = monkeys[index]
    target_monkey.starting_items.append(new_item)

    return None


def process_round(
    monkeys: List[Monkey], counts: List[int]
) -> Tuple[List[Monkey], List[int]]:
    for monkey in monkeys:
        while len(monkey.starting_items) > 0:
            item = monkey.starting_items.pop(0)
            new_item = do_expression(monkey.expression, item)
            new_item = div_by_3(new_item)
            pass_item(monkey, new_item, monkeys)

            counts[monkey._id] += 1
    return monkeys, counts


def process_round2(
    monkeys: List[Monkey], counts: List[int]
) -> Tuple[List[Monkey], List[int]]:
    for monkey in monkeys:
        while len(monkey.starting_items) > 0:
            item = monkey.starting_items.pop(0)
            new_item = do_expression(monkey.expression, item)
            # see: https://chasingdings.com/2022/12/11/advent-of-code-day-11-monkey-in-the-middle/
            new_item = new_item % 9699690
            pass_item(monkey, new_item, monkeys)

            counts[monkey._id] += 1
    return monkeys, counts


def partX(part: int):
    """
    Monkey business.
    """
    monkeys: List[Monkey] = []

    with open("input.txt") as f:
        lines = f.readlines()

        monkey_str = ""
        for line in lines:
            line = line.strip()
            monkey_str += f"{line}\n"
            if not line:
                monkeys.append(parse_monkey(monkey_str))
                monkey_str = ""
        monkeys.append(parse_monkey(monkey_str))

    # for monkey in monkeys:
    #     print(monkey)

    counts = [0] * len(monkeys)

    for i in range(ROUNDS):
        # print(f"=== ROUND {i} ===")
        monkeys, counts = (
            process_round(monkeys, counts)
            if part == 1
            else process_round2(monkeys, counts)
        )
        # print(counts)

    max_count = max(counts)
    counts.remove(max_count)
    max2_count = max(counts)

    print(max_count * max2_count)


if __name__ == "__main__":
    partX(part=1)
    partX(part=2)
