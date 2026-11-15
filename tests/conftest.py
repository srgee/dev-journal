# tests/conftest.py
import pytest

from journal.db import JournalDatabase


@pytest.fixture
def db_file(tmp_path):
    path = tmp_path / "journal.json"
    path.touch()
    return path


@pytest.fixture
def db(db_file):
    return JournalDatabase(db_file)
