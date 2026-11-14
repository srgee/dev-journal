import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from main import (
    MAX_CONTENT_LENGTH,
    MAX_TITLE_LENGTH,
    JournalEntry,
    add_entry,
    app,
    load_entries,
    match_query,
    save_entries,
)


@pytest.fixture
def db_file(tmp_path):
    path = tmp_path / "journal.json"
    path.touch()
    return path


@pytest.fixture
def runner():
    return CliRunner()


def test_create_valid_entry():
    entry = JournalEntry(title="Test Title", content="Test content")
    assert entry.title == "Test Title"
    assert entry.tags == []
    assert entry.date is not None


def test_each_entry_gets_own_tag_list():
    entry1 = JournalEntry(title="First", content="Content")
    entry2 = JournalEntry(title="Second", content="Content")
    entry1.tags.append("python")
    assert entry2.tags == []


def test_empty_title():
    with pytest.raises(ValueError):
        JournalEntry(title="", content="Valid")


def test_title_too_long():
    with pytest.raises(ValueError):
        JournalEntry(title="T" * (MAX_TITLE_LENGTH + 1), content="Valid")


def test_content_too_long():
    with pytest.raises(ValueError):
        JournalEntry(title="Valid", content="C" * (MAX_CONTENT_LENGTH + 1))


def test_save_and_load_entries(db_file):
    entries = [
        JournalEntry(title="First", content="Content 1", tags=["tag1"]),
        JournalEntry(title="Second", content="Content 2", tags=["tag2"]),
    ]
    save_entries(entries, db_file)
    loaded = load_entries(db_file)
    assert len(loaded) == 2
    assert loaded[0].tags == ["tag1"]
    assert loaded[1].tags == ["tag2"]


def test_load_entries_nonexistent_file():
    assert load_entries(Path("nonexistent.json")) == []


def test_save_entries_creates_valid_json(db_file):
    save_entries([JournalEntry(title="Test", content="Content")], db_file)
    with open(db_file) as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert data[0]["title"] == "Test"


def test_add_multiple_entries(db_file):
    add_entry("First", "Content 1", ["tag1"], db_file)
    add_entry("Second", "Content 2", ["tag2"], db_file)
    entries = load_entries(db_file)
    assert len(entries) == 2
    assert entries[0].title == "First"
    assert entries[1].title == "Second"


def test_cli_add_with_flags(db_file, runner):
    result = runner.invoke(
        app,
        [
            "add",
            "--title",
            "CLI Entry",
            "--content",
            "Added via CLI",
            "--tags",
            "python, cli",
            "--db-path",
            str(db_file),
        ],
    )
    assert result.exit_code == 0
    assert "Entry saved" in result.output


def test_cli_add_invalid_title(db_file, runner):
    result = runner.invoke(
        app,
        [
            "add",
            "--title",
            "",
            "--content",
            "Valid content",
            "--tags",
            "",
            "--db-path",
            str(db_file),
        ],
    )
    assert result.exit_code != 0


def test_cli_list_entries(db_file, runner):
    add_entry("Entry One", "Content 1", ["tag1"], db_file)
    add_entry("Entry Two", "Content 2", ["tag2"], db_file)
    result = runner.invoke(app, ["list", "--db-path", str(db_file)])
    assert result.exit_code == 0
    assert "Entry One" in result.output
    assert "Entry Two" in result.output


def test_cli_list_empty(db_file, runner):
    result = runner.invoke(app, ["list", "--db-path", str(db_file)])
    assert result.exit_code == 0
    assert "no" in result.output.lower()


def test_match_query_title():
    entry = JournalEntry(title="Python Basics", content="Content", tags=["python"])
    assert match_query(entry, "python")


def test_match_query_case_insensitive():
    entry = JournalEntry(title="PYTHON Basics", content="Content", tags=[])
    assert match_query(entry, "python")


def test_match_query_content_and_tags():
    entry = JournalEntry(title="Entry", content="I love pytest", tags=["tooling"])
    assert match_query(entry, "pytest")
    assert match_query(entry, "tool")  # matches the tag
    assert not match_query(entry, "nonexistent")


def test_cli_search(db_file, runner):
    add_entry("Python Tips", "Use list comprehensions", ["python"], db_file)
    add_entry("Rust Guide", "Ownership model", ["rust"], db_file)
    result = runner.invoke(app, ["search", "python", "--db-path", str(db_file)])
    assert result.exit_code == 0
    assert "Python Tips" in result.output
    assert "Rust Guide" not in result.output


def test_cli_search_no_results(db_file, runner):
    add_entry("Entry", "Content", ["tag"], db_file)
    result = runner.invoke(app, ["search", "nope", "--db-path", str(db_file)])
    assert result.exit_code == 0
    assert "no" in result.output.lower()


def test_cli_list_with_tag(db_file, runner):
    add_entry("Python Entry", "Content", ["python"], db_file)
    add_entry("Rust Entry", "Content", ["rust"], db_file)
    result = runner.invoke(app, ["list", "--tags", "python", "--db-path", str(db_file)])
    assert result.exit_code == 0
    assert "Python Entry" in result.output
    assert "Rust Entry" not in result.output


def test_cli_list_with_limit(db_file, runner):
    for title in ("First", "Second", "Third"):
        add_entry(title, "Content", [], db_file)
    result = runner.invoke(app, ["list", "--limit", "2", "--db-path", str(db_file)])
    assert result.exit_code == 0
    assert "Third" in result.output
    assert "Second" in result.output
    assert "First" not in result.output
