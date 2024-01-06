from abc import ABC
from dataclasses import dataclass
from functools import cache
from numbers import Number
from typing import TypeVar

NUM = TypeVar("NUM", int, float)


class Expr(ABC):

    def eval(self, variables: dict[str, "NUM | Expr"]) -> NUM:
        raise NotImplementedError()

    def expand(self, variables: dict[str, "NUM | Expr"]) -> "Expr":
        raise NotImplementedError()

    def simplify(self) -> "Expr":
        raise NotImplementedError()

    def contains_variable(self, name: str) -> bool:
        raise NotImplementedError()


@dataclass
class Const(Expr):
    val: NUM

    def eval(self, variables: dict[str, NUM | Expr]) -> NUM:
        return self.val

    def expand(self, variables: dict[str, "NUM | Expr"]) -> "Expr":
        return self

    def simplify(self) -> "Expr":
        return self

    def contains_variable(self, name: str) -> bool:
        return False

    def __str__(self):
        return str(self.val)


@dataclass
class Var(Expr):
    name: str

    def eval(self, variables: dict[str, NUM | Expr]) -> NUM:
        if isinstance(variables[self.name], Number):
            return variables[self.name]
        return variables[self.name].eval(variables)

    def expand(self, variables: dict[str, "NUM | Expr"]) -> "Expr":
        if self.name not in variables:
            return self
        if isinstance(variables[self.name], Number):
            return Const(variables[self.name])
        return variables[self.name].expand(variables)

    def simplify(self) -> "Expr":
        return self

    def contains_variable(self, name: str) -> bool:
        return self.name == name

    def __str__(self):
        return self.name


@dataclass
class Add(Expr):
    lhs: Expr
    rhs: Expr

    def eval(self, variables: dict[str, NUM | Expr]) -> NUM:
        return self.lhs.eval(variables) + self.rhs.eval(variables)

    def expand(self, variables: dict[str, "NUM | Expr"]) -> "Expr":
        return Add(self.lhs.expand(variables), self.rhs.expand(variables))

    def simplify(self) -> "Expr":
        new_lhs = self.lhs.simplify()
        new_rhs = self.rhs.simplify()
        if isinstance(new_lhs, Const) and isinstance(new_rhs, Const):
            return Const(new_lhs.val + new_rhs.val)
        return Add(new_lhs, new_rhs)

    def contains_variable(self, name: str) -> bool:
        return self.rhs.contains_variable(name) or self.lhs.contains_variable(name)

    def __str__(self):
        return f"({str(self.lhs)} + {str(self.rhs)})"


@dataclass
class Sub(Expr):
    lhs: Expr
    rhs: Expr

    def eval(self, variables: dict[str, NUM | Expr]) -> NUM:
        return self.lhs.eval(variables) - self.rhs.eval(variables)

    def expand(self, variables: dict[str, "NUM | Expr"]) -> "Expr":
        return Sub(self.lhs.expand(variables), self.rhs.expand(variables))

    def simplify(self) -> "Expr":
        new_lhs = self.lhs.simplify()
        new_rhs = self.rhs.simplify()
        if isinstance(new_lhs, Const) and isinstance(new_rhs, Const):
            return Const(new_lhs.val - new_rhs.val)
        return Sub(new_lhs, new_rhs)

    def contains_variable(self, name: str) -> bool:
        return self.rhs.contains_variable(name) or self.lhs.contains_variable(name)

    def __str__(self):
        return f"({str(self.lhs)} - {str(self.rhs)})"


@dataclass
class Mul(Expr):
    lhs: Expr
    rhs: Expr

    def eval(self, variables: dict[str, NUM | Expr]) -> NUM:
        return self.lhs.eval(variables) * self.rhs.eval(variables)

    def expand(self, variables: dict[str, "NUM | Expr"]) -> "Expr":
        return Mul(self.lhs.expand(variables), self.rhs.expand(variables))

    def simplify(self) -> "Expr":
        new_lhs = self.lhs.simplify()
        new_rhs = self.rhs.simplify()
        if isinstance(new_lhs, Const) and isinstance(new_rhs, Const):
            return Const(new_lhs.val * new_rhs.val)
        return Mul(new_lhs, new_rhs)

    def contains_variable(self, name: str) -> bool:
        return self.rhs.contains_variable(name) or self.lhs.contains_variable(name)

    def __str__(self):
        return f"({str(self.lhs)} * {str(self.rhs)})"


@dataclass
class Div(Expr):
    lhs: Expr
    rhs: Expr

    def eval(self, variables: dict[str, NUM | Expr]) -> NUM:
        return self.lhs.eval(variables) / self.rhs.eval(variables)

    def contains_variable(self, name: str) -> bool:
        return self.rhs.contains_variable(name) or self.lhs.contains_variable(name)

    def expand(self, variables: dict[str, "NUM | Expr"]) -> "Expr":
        return Div(self.lhs.expand(variables), self.rhs.expand(variables))

    def simplify(self) -> "Expr":
        new_lhs = self.lhs.simplify()
        new_rhs = self.rhs.simplify()
        if isinstance(new_lhs, Const) and isinstance(new_rhs, Const):
            return Const(new_lhs.val / new_rhs.val)
        return Div(new_lhs, new_rhs)

    def __str__(self):
        return f"({str(self.lhs)} / {str(self.rhs)})"


def parse_expression(expr_s: str) -> Expr:
    if "+" in expr_s or "-" in expr_s:
        split_pos = max(expr_s.find("+"), expr_s.find("-"))
        lhs = parse_expression(expr_s[:split_pos].strip())
        rhs = parse_expression(expr_s[split_pos + 1 :].strip())
        if expr_s[split_pos] == "+":
            return Add(lhs, rhs)
        else:
            return Sub(lhs, rhs)

    if "*" in expr_s or "/" in expr_s:
        split_pos = max(expr_s.find("*"), expr_s.find("/"))
        lhs = parse_expression(expr_s[:split_pos].strip())
        rhs = parse_expression(expr_s[split_pos + 1 :].strip())
        if expr_s[split_pos] == "*":
            return Mul(lhs, rhs)
        else:
            return Div(lhs, rhs)

    try:
        return Const(int(expr_s))
    except ValueError:
        return Var(expr_s)
