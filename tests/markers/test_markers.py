import sys

import pytest


@pytest.mark.slow
def test_custom_marker_is_attached(request):
    assert request.node.get_closest_marker("slow") is not None


@pytest.mark.skip(reason="Demonstrates an intentionally skipped example")
def test_skip():
    raise AssertionError("A skipped test is not executed")


@pytest.mark.skipif(sys.platform == "win32", reason="Example is not for Windows")
def test_conditional_skip():
    assert sys.platform != "win32"


@pytest.mark.xfail(reason="Demonstrates a known, expected failure")
def test_expected_failure():
    assert 1 == 2
