from howtopytest.greetings import greeting


def test_tmp_path_writes_inside_a_temporary_directory(tmp_path):
    note = tmp_path / "note.txt"
    note.write_text("pytest fixture", encoding="utf-8")
    assert note.read_text(encoding="utf-8") == "pytest fixture"


def test_monkeypatch_restores_environment_after_test(monkeypatch):
    monkeypatch.setenv("HOWTOPYTEST_NAME", "Ada")
    assert greeting() == "Hello, Ada!"


def test_capsys_captures_output(capsys):
    print("captured output")
    captured = capsys.readouterr()
    assert captured.out == "captured output\n"
    assert captured.err == ""
