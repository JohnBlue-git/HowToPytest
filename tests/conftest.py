"""Fixtures available to every test below this directory."""

import pytest


@pytest.fixture
def sample_numbers():
    """A fresh value for tests that request it."""
    return [2, 4, 6]


@pytest.fixture(scope="session")
def project_name():
    """An immutable value shared for the duration of this pytest session."""
    return "HowToPytest"
