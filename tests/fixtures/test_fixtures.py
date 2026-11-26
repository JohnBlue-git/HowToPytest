import pytest


def test_shared_fixture_is_fresh_per_test(sample_numbers):
    sample_numbers.append(8)
    assert sample_numbers == [2, 4, 6, 8]


def test_shared_fixture_does_not_leak_mutation(sample_numbers):
    assert sample_numbers == [2, 4, 6]


def test_session_scoped_fixture(project_name):
    assert project_name == "HowToPytest"


@pytest.fixture
def resource_log():
    events = ["setup"]
    yield events
    events.append("teardown")


def test_yield_fixture_setup(resource_log):
    assert resource_log == ["setup"]


@pytest.fixture
def text_file(tmp_path):
    nested_file = tmp_path / "nested" / "note.txt"
    nested_file.parent.mkdir()
    nested_file.write_text("fixture dependency", encoding="utf-8")
    return nested_file


def test_fixture_can_depend_on_another_fixture(text_file):
    assert text_file.read_text(encoding="utf-8") == "fixture dependency"
