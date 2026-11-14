import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

import typer

MAX_TITLE_LENGTH = 50
MAX_CONTENT_LENGTH = 1000

app = typer.Typer()


@dataclass
class JournalEntry:
    title: str
    content: str
    tags: list[str] = field(default_factory=list)
    date: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        if not self.title or len(self.title) > MAX_TITLE_LENGTH:
            raise ValueError(
                f"Title must be non-empty and <= {MAX_TITLE_LENGTH} characters"
            )
        if not self.content or len(self.content) > MAX_CONTENT_LENGTH:
            raise ValueError(
                f"Content must be non-empty and <= {MAX_CONTENT_LENGTH} characters"
            )


def save_entries(entries: list[JournalEntry], db_path: Path) -> None:
    data = [asdict(e) for e in entries]
    with open(db_path, mode="w") as f:
        json.dump(data, f, indent=2)


def load_entries(db_path: Path) -> list[JournalEntry]:
    if not db_path.exists() or db_path.stat().st_size == 0:
        return []
    with open(db_path, mode="r") as f:
        data = json.load(f)
    return [JournalEntry(**e) for e in data]


def add_entry(title: str, content: str, tags: list[str], db_path: Path) -> None:
    entries = load_entries(db_path)
    entry = JournalEntry(title=title, content=content, tags=tags)
    entries.append(entry)  # append, don't overwrite
    save_entries(entries, db_path)


def match_query(entry: JournalEntry, query: str) -> bool:
    return (
        query.lower() in entry.title.lower()
        or query.lower() in entry.content.lower()
        or any(query.lower() in tag.lower() for tag in entry.tags)
    )


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
    try:
        add_entry(title, content, tag_list, db_path)
        print("✔ Entry saved successfully!")
    except ValueError as e:
        raise typer.BadParameter(str(e)) from e


@app.command("list")
def list_entries(
    tags: list[str] = typer.Option([], help="Filter by tag (repeatable)"),
    limit: int = typer.Option(0, help="Show last N entries (0 = all)"),
    db_path: Path = typer.Option(Path("journal.json"), hidden=True),
) -> None:
    entries = load_entries(db_path)
    if len(entries) == 0:
        print("No entries found.")
        return

    if tags:
        filtered_entries = [
            e for e in entries if any(match_query(e, tag) for tag in tags)
        ]
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
    entries = load_entries(db_path)
    found_entries = [e for e in entries if match_query(e, query)]
    if found_entries:
        for entry in found_entries:
            _display(entry)
    else:
        print("No entries found.")


if __name__ == "__main__":
    app()
