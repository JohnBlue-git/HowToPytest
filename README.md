# HowToPytest

A small, runnable project that teaches pytest by showing its features working
together. Examples live beside the feature they demonstrate, and the guide
connects those examples to pytest's collection, fixture, and test-running hooks.

## Run it

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

Useful focused runs:

```bash
python -m pytest tests/parametrize
python -m pytest -m "not slow"
python -m pytest --collect-only -q
python -m pytest tests/hooks -vv
```

## Project map

```text
.
├── docs/                    # Focused guides for configuration and concepts
├── pytest.ini               # Discovery rules, defaults, and registered markers
├── requirements-dev.txt     # Test runner dependency
├── src/howtopytest/         # Small application code under test (src layout)
└── tests/
    ├── conftest.py          # Fixtures shared by all test directories
    ├── builtin_fixtures/    # tmp_path, monkeypatch, capsys
    ├── classes/             # Class-based test collection
    ├── fixtures/            # Fixture scope, dependency, and teardown examples
    ├── hooks/                # pytest_generate_tests and collection hooks
    ├── markers/              # skip, skipif, xfail, and custom markers
    └── parametrize/          # Parameterized tests and readable case IDs
```

## Follow a test from source to result

1. `pytest.ini` selects `tests/`, defines test naming conventions, and enables
   strict marker/config validation.
2. Pytest loads `conftest.py` files as local plugins. The root file supplies
   shared fixtures; `tests/hooks/conftest.py` adds directory-local hooks.
3. Python test modules and functions are collected. The `pytest_generate_tests`
   example creates parameterized test cases dynamically; `pytest_collection_modifyitems`
   adds a marker after items have been collected.
4. Fixtures are resolved for each test. Built-in and project fixtures are
   constructed before the test and yield-fixture cleanup runs afterward.
5. Pytest runs setup, call, and teardown for each item, then creates reports.
   The test outcome (pass, fail, skip, or xfail) is visible in the terminal.

The [source-to-object mapping guide](docs/test-objects-and-markers.md)
explains how pytest's `File`/`Module`/`Class` collectors create `Function`
items, how decorators attach marks, and when each mark is acted on. The hook
declarations are in pytest's `src/_pytest/hookspec.py`; Python test collection
and parametrization are implemented in `src/_pytest/python.py`, fixture
resolution in `src/_pytest/fixtures.py`, and the setup/call/teardown protocol
and reports in `src/_pytest/runner.py`. These are pytest internals (not APIs to
import from this project); hook names in the examples are the supported
extension points.

| Project example | Pytest object / mechanism | Implementation area |
| --- | --- | --- |
| [`pytest.ini`](pytest.ini) | Configuration used by path and Python collectors | `src/_pytest/config/`, `src/_pytest/python.py` |
| [`tests/classes/`](tests/classes) | `pytest.File` → Python `Module` → `Class` collector → `Function` item | `src/_pytest/python.py` |
| Decorators in [`tests/parametrize/`](tests/parametrize) | `Mark` → `Metafunc` → `CallSpec2` → multiple `Function` items | `src/_pytest/mark/structures.py`, `src/_pytest/python.py` |
| [`tests/markers/`](tests/markers) | Marks attached to collected item; selection or skip/xfail behavior | `src/_pytest/mark/`, `src/_pytest/skipping.py` |
| [`tests/conftest.py`](tests/conftest.py), [`tests/fixtures/`](tests/fixtures) | Fixture definitions resolved for a `Function` item | `src/_pytest/config/`, `src/_pytest/fixtures.py` |
| [`tests/hooks/conftest.py`](tests/hooks/conftest.py) | Hook implementations alter collection/items; not test items | `src/_pytest/hookspec.py`, `src/_pytest/python.py` |
| [`tests/builtin_fixtures/`](tests/builtin_fixtures) | Built-in fixture providers (`tmp_path`, `monkeypatch`, `capsys`) | `src/_pytest/tmpdir.py`, `src/_pytest/monkeypatch.py`, `src/_pytest/capture.py` |
| All test outcomes | Runtest phases and reports for each `Function` item | `src/_pytest/runner.py` |

See [the hook and lifecycle guide](docs/hooks-and-lifecycle.md),
[the source-to-object mapping guide](docs/test-objects-and-markers.md),
[configuration and discovery](docs/configuration-and-discovery.md),
[fixtures](docs/fixtures.md), and [project layout](docs/project-layout.md)
for the details and commands to inspect each step.

This project demonstrates common pytest features, not every third-party plugin
or every hook in pytest. The [pytest hook reference](https://docs.pytest.org/en/stable/reference/reference.html#hooks)
lists the full hook API.
