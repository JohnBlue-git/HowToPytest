import pytest

from howtopytest.math_tools import add, divide, is_even


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        pytest.param(1, 2, 3, id="positive"),
        pytest.param(-1, 1, 0, id="cancellation"),
        pytest.param(0, 0, 0, id="zeros"),
    ],
)
def test_add(left, right, expected):
    assert add(left, right) == expected


@pytest.mark.parametrize("number", range(0, 7), ids=lambda number: f"n={number}")
def test_even_numbers(number):
    assert is_even(number) is (number % 2 == 0)


@pytest.mark.parametrize(
    ("numerator", "denominator", "expected"),
    [(6, 3, 2), (-8, 2, -4)],
)
def test_divide(numerator, denominator, expected):
    assert divide(numerator, denominator) == expected


def test_divide_by_zero_raises_a_specific_exception():
    with pytest.raises(ValueError, match="denominator must not be zero"):
        divide(1, 0)
