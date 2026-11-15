from pathlib import Path

from journal.db import JournalDatabase


def test_load_empty_database(db):
    assert db.load_entries() == []


def test_return_empty_list_for_missing_db():
    db = JournalDatabase(Path("missing.json"))
    assert db.load_entries() == []


def test_add_entry(db):
    db.add_entry("Title", "Content", ["tag"])
    entries = db.load_entries()
    assert len(entries) == 1
    assert entries[0].title == "Title"
    assert entries[0].tags == ["tag"]


def test_add_multiple_entries(db):
    db.add_entry("First", "Content 1", ["tag1"])
    db.add_entry("Second", "Content 2", ["tag2"])
    assert len(db.load_entries()) == 2


def test_search_by_title(db):
    db.add_entry("Python Basics", "Content", ["python"])
    db.add_entry("Rust Intro", "Content", ["rust"])
    results = JournalDatabase.search_entries(
        db.load_entries(), "python", titles_only=True
    )
    assert len(results) == 1
    assert results[0].title == "Python Basics"


def test_search_by_content_and_tags(db):
    db.add_entry("Entry", "I love pytest", ["tooling"])
    entries = db.load_entries()
    assert len(JournalDatabase.search_entries(entries, "pytest")) == 1
    assert len(JournalDatabase.search_entries(entries, "tool")) == 1  # tag match


def test_search_case_insensitive(db):
    db.add_entry("PYTHON Entry", "Content", [])
    results = JournalDatabase.search_entries(db.load_entries(), "python")
    assert len(results) == 1


def test_search_titles_only(db):
    db.add_entry(title="Title has python", content="content has rust", tags=[])
    entries = db.load_entries()
    assert len(JournalDatabase.search_entries(entries, "rust", titles_only=True)) == 0
    assert len(JournalDatabase.search_entries(entries, "python", titles_only=True)) == 1


def test_search_no_match(db):
    db.add_entry("Entry", "Content", [])
    assert db.search_entries(db.load_entries(), "nonexistent") == []
