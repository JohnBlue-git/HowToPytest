# From test source to pytest objects

The decorators in test code do not all mean “make this a test.” Pytest has a
collection tree, and its Python collector turns matching Python objects into
pytest nodes. Marks and fixtures are metadata interpreted at different points
in that process.

## Object creation path

For a Python test file such as
[`tests/parametrize/test_parametrize.py`](../tests/parametrize/test_parametrize.py),
the simplified path is:

```text
filesystem path
  -> pytest_collect_file hook
  -> _pytest.python.Module (a pytest.File collector)
  -> pytest_pycollect_makeitem(collector, name, obj)
  -> _pytest.python.Class collector, when obj is a matching Test* class
  -> _pytest.python.Function item, when obj is a matching test_* function
  -> setup/call/teardown for each Function item
```

In pytest 8.x, the Python file collector is the internal
`_pytest.python.Module`, which subclasses `pytest.File`. A class is represented
by `_pytest.python.Class` (a collector), and a runnable Python test is
`_pytest.python.Function` (an item, ultimately a `pytest.Item`). The `pytest`
prefixes in the public API are not necessarily the concrete internal class
names.

The relevant implementation is in pytest's `src/_pytest/python.py`:

1. `pytest_collect_file` accepts a path matching `python_files`.
2. `pytest_pycollect_makemodule` creates a `Module` collector for that path.
3. `PyCollector.collect` inspects module/class attributes and calls
   `pytest_pycollect_makeitem`.
4. `pytest_pycollect_makeitem` applies the configured class/function naming
   rules and creates a class collector or function item.

So `pytest.File` is a base node type, not a component that looks for every
decorator. Pytest's Python plugin supplies the more specific `Module` behavior.
Other plugins can define collectors for other file types.

## What the syntax maps to

| Test-code syntax | What Python stores / pytest recognizes | Effect on pytest objects | Main pytest implementation |
| --- | --- | --- | --- |
| `def test_x(): ...` | A Python function with a name matching `python_functions` | The Python collector creates one `Function` item. | `pytest_collect_file`, `PyCollector.collect`, `pytest_pycollect_makeitem` in `src/_pytest/python.py` |
| `class TestX: ...` | A Python class matching `python_classes` | Creates a `Class` collector; matching methods become `Function` items. | `pytest_pycollect_makeitem`, `Class.collect` in `src/_pytest/python.py` |
| `@pytest.mark.slow` | A `MarkDecorator` applies a `Mark` to the object's `pytestmark` attribute | The eventual item carries the mark; `-m slow` selects it. A custom mark alone does not change execution. | `MarkDecorator` in `src/_pytest/mark/structures.py`; `-m` selection in `src/_pytest/mark/` |
| `@pytest.mark.skip(...)` / `skipif(...)` | A mark attached to the function/class | The skipping plugin checks it during runtest setup and reports a skipped outcome. | `pytest_runtest_setup`, `pytest_runtest_makereport` in `src/_pytest/skipping.py` |
| `@pytest.mark.xfail(...)` | A mark attached to the function/class | The skipping plugin interprets the result and reports xfail/xpass; `strict` controls whether an unexpected pass fails. | `pytest_runtest_setup`, `pytest_runtest_makereport` in `src/_pytest/skipping.py` |
| `@pytest.mark.parametrize(...)` | A `parametrize` mark attached to the function | The built-in `pytest_generate_tests` reads it into `Metafunc.parametrize`; each callspec becomes its own `Function` item, usually with `[id]` appended. | Built-in `pytest_generate_tests`, `Metafunc.parametrize`, `_genfunctions` in `src/_pytest/python.py` |
| `pytest.param(..., marks=...)` | A parameter set containing values, optional ID, and marks | Its marks are attached to the corresponding generated item, not the entire function. | `ParameterSet` / `CallSpec2` in `src/_pytest/mark/structures.py` and `src/_pytest/python.py` |
| `@pytest.fixture` | A `FixtureFunctionMarker` wraps/registers a fixture definition | Not a test item. The fixture manager resolves a matching test argument, runs setup and cleanup, and supplies its value to the `Function`. | `FixtureFunctionMarker`, `FixtureManager`, `pytest_fixture_setup` in `src/_pytest/fixtures.py` |
| `def pytest_generate_tests(metafunc): ...` | A hook implementation registered from a plugin or `conftest.py` | Called during collection to add parametrization; it is not itself collected as a test. | Hook spec in `src/_pytest/hookspec.py`; call in `src/_pytest/python.py` |
| `def pytest_collection_modifyitems(items): ...` | A hook implementation registered from a plugin or `conftest.py` | Called with already-created items so plugins can reorder, deselect, or mark them. | Hook spec in `src/_pytest/hookspec.py`; implementations in plugins such as `src/_pytest/mark/` |

`@pytest.mark` and `@pytest.mark.parametrize` use the same decorator/mark
machinery, but have different consumers. The built-in
`pytest_generate_tests` implementation in `src/_pytest/python.py` specifically
looks for marks named `parametrize` and turns them into callspecs. By contrast,
the mark-selection plugin handles `-m`, and `src/_pytest/skipping.py` handles
skip/xfail semantics. An arbitrary registered mark is just metadata until a
selection expression or plugin gives it behavior.

Fixture decorators are not marks. `@pytest.fixture` declares a fixture
definition; the fixture manager discovers definitions from test modules and
`conftest.py`, builds the fixture dependency closure from function arguments,
and supplies values during setup. In this repository,
[`tests/conftest.py`](../tests/conftest.py) defines shared fixtures and
[`tests/fixtures/test_fixtures.py`](../tests/fixtures/test_fixtures.py) shows a
fixture depending on another fixture.

## Concrete parametrization mapping

In `test_add`, `@pytest.mark.parametrize` attaches one mark containing
`("left", "right", "expected")` and three parameter sets. During collection:

```text
one Python function definition
  -> one FunctionDefinition / Metafunc
  -> three CallSpec2 objects
  -> three Function items:
       test_add[positive]
       test_add[cancellation]
       test_add[zeros]
```

The number of collected test items grows from 1 to 3; pytest calls the same
underlying Python function once per item with that item's arguments. See
[`tests/parametrize/test_parametrize.py`](../tests/parametrize/test_parametrize.py)
and verify the IDs with:

```bash
python -m pytest --collect-only -q tests/parametrize
```

The explicit hook example in
[`tests/hooks/conftest.py`](../tests/hooks/conftest.py) uses the same
`Metafunc.parametrize` mechanism directly. It turns the `currency` argument
into the two items ending in `[dollar]` and `[euro]`.

## Marks and execution phases

```text
decorator
  -> MarkDecorator applies Mark metadata to Python object's pytestmark
  -> collector copies marks to the collected item
  -> collection hooks / -m selection can inspect item marks
  -> runtest setup checks skip/skipif
  -> test call runs (unless skipped or xfail(run=False))
  -> report hook interprets pass/fail as passed, failed, skipped,
     xfailed, or xpassed
```

The mark decorator implementation is in `src/_pytest/mark/structures.py`;
marker selection is in `src/_pytest/mark/`; skip/xfail interpretation is in
`src/_pytest/skipping.py`; and the generic runtest protocol is in
`src/_pytest/runner.py`. These are pytest implementation details, not imports
for application tests.

Try:

```bash
python -m pytest --collect-only -q
python -m pytest -m slow -vv
python -m pytest tests/markers -vv
```
