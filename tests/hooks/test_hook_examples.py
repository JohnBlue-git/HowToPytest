import pytest


def test_currency_values_are_generated_during_collection(currency):
    assert currency in {"USD", "EUR"}


def test_collection_hook_was_applied(request):
    assert request.node.get_closest_marker("from_collection_hook") is not None
