"""Hooks scoped to tests in this directory."""

import pytest


def pytest_generate_tests(metafunc):
    """Generate inputs for tests that request the `currency` argument."""
    if "currency" in metafunc.fixturenames:
        metafunc.parametrize("currency", ["USD", "EUR"], ids=["dollar", "euro"])


def pytest_collection_modifyitems(items):
    """Mark one collected item so its test can prove this hook ran."""
    for item in items:
        if item.name == "test_collection_hook_was_applied":
            item.add_marker(pytest.mark.from_collection_hook)
