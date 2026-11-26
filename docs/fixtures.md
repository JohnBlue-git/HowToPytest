# Fixtures

[`tests/conftest.py`](../tests/conftest.py) contains shared fixtures. A test
requests a fixture by naming it as a function argument; pytest resolves fixture
dependencies and supplies the returned value. Fixtures are function-scoped by
default, as shown by the independent `sample_numbers` values.

`project_name` uses session scope, so pytest can reuse it during one test
session. The `resource_log` fixture in
[`tests/fixtures/test_fixtures.py`](../tests/fixtures/test_fixtures.py) uses
`yield`: code before `yield` is setup and code after it is teardown. Pytest
ensures teardown runs even when a test fails.

The built-in `tmp_path`, `monkeypatch`, and `capsys` fixtures show how pytest
provides isolated resources without a project-defined fixture. Fixture setup
is driven by the `pytest_fixture_setup` hook; the fixture manager resolves
dependencies and scope, and finalizers perform cleanup at the appropriate
scope boundary.

Run `python -m pytest tests/fixtures tests/builtin_fixtures -vv` to focus on
these examples.
