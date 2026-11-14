import pytest

from journal.models import MAX_CONTENT_LENGTH, MAX_TITLE_LENGTH, JournalEntry


def test_create_journal_entry_for_valid_data():
    entry = JournalEntry(title="Test", content="Content")
    assert entry.title == "Test"
    assert entry.tags == []
    assert entry.date is not None


def test_raise_value_error_when_title_is_empty():
    with pytest.raises(ValueError):
        JournalEntry(title="", content="Valid")


def test_raise_value_error_when_title_is_too_long():
    with pytest.raises(ValueError):
        JournalEntry(title="T" * (MAX_TITLE_LENGTH + 1), content="Valid")


def test_raise_value_error_when_title_is_none():
    with pytest.raises(ValueError):
        JournalEntry(title=None, content="")


def test_raise_value_error_when_content_is_empty():
    with pytest.raises(ValueError):
        JournalEntry(title="Valid", content="")


def test_raise_value_error_when_content_is_too_long():
    with pytest.raises(ValueError):
        JournalEntry(title="Valid", content="C" * (MAX_CONTENT_LENGTH + 1))


def test_initialize_entry_with_independent_tag_list():
    a = JournalEntry(title="A", content="C")
    b = JournalEntry(title="B", content="C")
    a.tags.append("python")
    assert b.tags == []
