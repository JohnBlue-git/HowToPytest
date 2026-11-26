"""Simple functions for demonstrating pytest's core test features."""


def add(left: int, right: int) -> int:
    return left + right


def divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        raise ValueError("denominator must not be zero")
    return numerator / denominator


def is_even(number: int) -> bool:
    return number % 2 == 0
