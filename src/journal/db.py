import json
from dataclasses import asdict
from pathlib import Path

from .models import JournalEntry


class JournalDatabase:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def load_entries(self) -> list[JournalEntry]:
        if not self.db_path.exists() or self.db_path.stat().st_size == 0:
            return []
        with open(self.db_path, mode="r") as f:
            data = json.load(f)
        return [JournalEntry(**e) for e in data]

    def save_entries(self, entries: list[JournalEntry]) -> None:
        with open(self.db_path, mode="w") as f:
            json.dump([asdict(e) for e in entries], f, indent=2)

    def add_entry(self, title: str, content: str, tags: list[str], db_path: Path) -> None:
        entries = self.load_entries()
        entries.append(JournalEntry(title=title, content=content, tags=tags))
        self.save_entries(entries)

    @staticmethod
    def search_entries(entries: list[JournalEntry], query: str, titles_only: bool = False) -> list[JournalEntry]:
        result = []
        for e in entries:
            if titles_only and query.lower() in e.title.lower():
                result.append(e)
                continue
            if query.lower() in e.content:
                result.append(e)
            if any(query.lower() in tag.lower() for tag in e.tags):
                result.append(e)
        return result
