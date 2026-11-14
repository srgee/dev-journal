from pathlib import Path

import typer

from .db import JournalDatabase
from .models import JournalEntry

app = typer.Typer()


def _display(entry: JournalEntry) -> None:
    print(f"Title: {entry.title}")
    print(f"Content: {entry.content}")
    print(f"Tags: {', '.join(entry.tags)}")
    print(f"Date: {entry.date}")
    print("---")


@app.command()
def add(
    title: str = typer.Option("", prompt="Title", show_default=False),
    content: str = typer.Option("", prompt="Content", show_default=False),
    tags: str = typer.Option("", prompt="Tags", show_default=False),
    db_path: Path = typer.Option(Path("journal.json"), hidden=True),
) -> None:
    tag_list = tags.split(",")
    db = JournalDatabase(db_path)
    try:
        db.add_entry(title, content, tag_list, db_path)
        print("✔ Entry saved successfully!")
    except ValueError as e:
        raise typer.BadParameter(str(e)) from e


@app.command("list")
def list_entries(
    tags: list[str] = typer.Option([], help="Filter by tag (repeatable)"),
    limit: int = typer.Option(0, help="Show last N entries (0 = all)"),
    db_path: Path = typer.Option(Path("journal.json"), hidden=True),
) -> None:
    db = JournalDatabase(db_path)
    entries = db.load_entries()
    if len(entries) == 0:
        print("No entries found.")
        return

    if tags:
        filtered_entries = []
        for tag in tags:
            filtered_entries += db.search_entries(entries, tag, False)
        if limit > 0:
            filtered_entries = filtered_entries[-limit:]
    elif limit > 0:
        filtered_entries = entries[-limit:]
    else:
        filtered_entries = entries

    for entry in filtered_entries:
        _display(entry)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search term"),
    db_path: Path = typer.Option(Path("journal.json"), hidden=True),
) -> None:
    db = JournalDatabase(db_path)
    entries = db.load_entries()
    if found_entries := db.search_entries(entries, query, False):
        for entry in found_entries:
            _display(entry)
    else:
        print("No entries found.")
