from howtopytest.math_tools import add


class TestCalculator:
    """Pytest collects Test* classes and their test_* methods."""

    def test_add_in_class(self):
        assert add(2, 3) == 5

    def test_another_method(self):
        assert add(-2, 2) == 0
