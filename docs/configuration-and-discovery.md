# Configuration and test discovery

The root [`pytest.ini`](../pytest.ini) keeps the runner's default behavior
visible and reproducible:

- `testpaths = tests` chooses where a bare `pytest` starts looking.
- `python_files`, `python_classes`, and `python_functions` define the default
  filename, class, and function naming patterns.
- `pythonpath = src` makes the `src/` layout importable without installing this
  teaching package.
- `markers` registers custom marks. `--strict-markers` makes a typo an error.
- `--strict-config` rejects unknown configuration options.
- `xfail_strict = true` makes an unexpected pass of an expected-failure test
  fail the suite.

Try `python -m pytest --collect-only -q` to see test items before execution.
Use `python -m pytest tests/parametrize -vv` to see individual parameter IDs,
or `python -m pytest -m slow` to select by marker.

The built-in Python collector applies naming rules and discovers test modules,
classes, and functions. A `conftest.py` is loaded as a local plugin, so its
fixtures and hooks apply to tests in its directory tree without imports from
test files.
