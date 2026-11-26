# Project layout and test classes

Application code uses the `src/howtopytest/` layout; tests are grouped by
pytest feature under `tests/`. The matching `test_*.py` names are discovered
using `pytest.ini` defaults. Shared fixtures belong in the nearest applicable
`conftest.py`; a nested conftest can provide local fixtures or hook
implementations without becoming an importable test module.

[`tests/classes/test_test_classes.py`](../tests/classes/test_test_classes.py)
shows the supported `Test*` / `test_*` class style. Methods must not define an
`__init__` constructor; pytest creates a fresh instance per test method.
Functions remain the simpler default, and class grouping is useful when tests
share a conceptual subject (not mutable setup state).

Run `python -m pytest --collect-only -q` after changing filenames or naming
patterns to check what pytest will collect.
