# Hooks and the pytest lifecycle

Pytest is extensible through hookspecs, with hook implementations provided by
plugins and `conftest.py` files. The examples in
[`tests/hooks/conftest.py`](../tests/hooks/conftest.py) are normal pytest hook
implementations, loaded locally for the hook examples directory.

## What the examples demonstrate

- `pytest_generate_tests(metafunc)` runs during Python test collection. It
  detects a test requesting `currency` and parameterizes it into two items.
  This is the hook-based counterpart to the `@pytest.mark.parametrize`
  decorator.
- `pytest_collection_modifyitems(items)` runs after collection. It attaches a
  marker to one item; the test queries that marker through its `request` fixture
  to prove the hook ran.
- `pytest_fixture_setup` is the hook pytest's fixture manager uses to set up
  fixtures. Project fixtures are declared with `@pytest.fixture`, rather than
  implementing this lower-level hook directly.
- The runtest protocol calls `pytest_runtest_setup`, `pytest_runtest_call`,
  and `pytest_runtest_teardown`. `pytest_runtest_makereport` creates reports
  for those phases. A skip or xfail mark affects whether/how the item is run
  and reported; it does not change the test discovery naming rules.

## Approximate execution path

```text
configuration + plugin/conftest loading
    -> collection of files, classes, functions
    -> pytest_generate_tests creates parameterized items
    -> pytest_collection_modifyitems can change collected items
    -> fixture setup
    -> runtest setup -> call -> teardown
    -> reports and session summary
```

Hook names are defined in pytest's `src/_pytest/hookspec.py`. Python object
collection and decorator-based parametrization are in `src/_pytest/python.py`;
fixture behavior is in `src/_pytest/fixtures.py`; skip/xfail behavior is in
`src/_pytest/skipping.py`; and the runtest protocol/reporting is in
`src/_pytest/runner.py`. Configuration and local-plugin loading are in
`src/_pytest/config/`. Built-in fixtures are implemented in modules such as
`src/_pytest/tmpdir.py`, `src/_pytest/monkeypatch.py`, and
`src/_pytest/capture.py`.

These are pytest implementation paths, not files in this repository. They can
be browsed in the source checkout or in the installed pytest package. They
explain the lifecycle; application tests should use the documented hooks and
fixture APIs, not import private `_pytest` modules.

Run `python -m pytest tests/hooks --collect-only -vv` to inspect generated
items, then `python -m pytest tests/hooks -vv` to see them execute.
