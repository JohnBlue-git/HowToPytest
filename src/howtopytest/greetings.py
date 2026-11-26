"""A tiny environment-dependent function for monkeypatch examples."""

import os


def greeting() -> str:
    name = os.getenv("HOWTOPYTEST_NAME", "pytest learner")
    return f"Hello, {name}!"
