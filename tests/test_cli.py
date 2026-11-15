import pytest
from typer.testing import CliRunner

from journal.cli import app
from journal.models import MAX_TITLE_LENGTH


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_add_success(db_file, runner):
    result = runner.invoke(
        app,
        [
            "add",
            "--title",
            "Test Entry",
            "--content",
            "Test content",
            "--tags",
            "python, testing",
            "--db-path",
            str(db_file),
        ],
    )
    assert result.exit_code == 0
    assert "saved" in result.output.lower()


def test_cli_add_failure(db_file, runner):
    result = runner.invoke(
        app,
        [
            "add",
            "--title",
            "T" * (MAX_TITLE_LENGTH + 1),
            "--content",
            "Valid",
            "--tags",
            "",
            "--db-path",
            str(db_file),
        ],
    )
    assert result.exit_code != 0


def test_cli_list_entries(db, db_file, runner):
    db.add_entry("Entry One", "Content 1", ["tag1"])
    db.add_entry("Entry Two", "Content 2", ["tag2"])
    result = runner.invoke(app, ["list", "--db-path", str(db_file)])
    assert result.exit_code == 0
    assert "Entry One" in result.output
    assert "Entry Two" in result.output


def test_cli_list_empty(db_file, runner):
    result = runner.invoke(app, ["list", "--db", str(db_file)])
    assert "no" in result.output.lower()


def test_cli_search(db, db_file, runner):
    db.add_entry("Python Tips", "Use comprehensions", ["python"])
    db.add_entry("Rust Guide", "Ownership model", ["rust"])
    result = runner.invoke(app, ["search", "python", "--db-path", str(db_file)])
    assert "Python Tips" in result.output
    assert "Rust Guide" not in result.output


def test_cli_search_empty(db_file, runner):
    result = runner.invoke(app, ["search", "nonexistent", "--db-path", str(db_file)])
    assert "no" in result.output.lower()


def test_cli_list_with_tag(db, db_file, runner):
    db.add_entry("Python Entry", "Content", ["python"])
    db.add_entry("Rust Entry", "Content", ["rust"])
    result = runner.invoke(app, ["list", "--tags", "python", "--db-path", str(db_file)])
    assert "Python Entry" in result.output
    assert "Rust Entry" not in result.output


def test_cli_list_with_limit(db, db_file, runner):
    for title in ("First", "Second", "Third"):
        db.add_entry(title, "Content", [])
    result = runner.invoke(app, ["list", "--limit", "2", "--db-path", str(db_file)])
    assert "Third" in result.output
    assert "Second" in result.output
    assert "First" not in result.output
