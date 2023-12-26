from abc import ABC
from dataclasses import dataclass
from typing import TypeVar

NUM = TypeVar("NUM", int, float)


class Expr(ABC):
    def eval(self, variables: dict[str, NUM]) -> NUM:
        raise NotImplementedError()


@dataclass
class Const(Expr):
    val: NUM

    def eval(self, variables: dict[str, NUM]) -> NUM:
        return self.val


@dataclass
class Var(Expr):
    name: str

    def eval(self, variables: dict[str, NUM]) -> NUM:
        return variables[self.name]


@dataclass
class Add(Expr):
    lhs: Expr
    rhs: Expr

    def eval(self, variables: dict[str, NUM]) -> NUM:
        return self.lhs.eval(variables) + self.rhs.eval(variables)

@dataclass
class Sub(Expr):
    lhs: Expr
    rhs: Expr

    def eval(self, variables: dict[str, NUM]) -> NUM:
        return self.lhs.eval(variables) - self.rhs.eval(variables)


@dataclass
class Mul(Expr):
    lhs: Expr
    rhs: Expr

    def eval(self, variables: dict[str, NUM]) -> NUM:
        return self.lhs.eval(variables) * self.rhs.eval(variables)


@dataclass
class Div(Expr):
    lhs: Expr
    rhs: Expr

    def eval(self, variables: dict[str, NUM]) -> NUM:
        return self.lhs.eval(variables) / self.rhs.eval(variables)


def parse_expression(expr_s: str) -> Expr:
    if "+" in expr_s or "-" in expr_s:
        split_pos = max(expr_s.find("+"), expr_s.find("-"))
        lhs = parse_expression(expr_s[:split_pos].strip())
        rhs = parse_expression(expr_s[split_pos + 1:].strip())
        if expr_s[split_pos] == "+":
            return Add(lhs, rhs)
        else:
            return Sub(lhs, rhs)

    if "*" in expr_s or "/" in expr_s:
        split_pos = max(expr_s.find("*"), expr_s.find("/"))
        lhs = parse_expression(expr_s[:split_pos].strip())
        rhs = parse_expression(expr_s[split_pos + 1:].strip())
        if expr_s[split_pos] == "*":
            return Mul(lhs, rhs)
        else:
            return Div(lhs, rhs)

    try:
        return Const(int(expr_s))
    except ValueError:
        return Var(expr_s)