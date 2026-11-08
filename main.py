import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

MAX_TITLE_LENGTH = 50
MAX_CONTENT_LENGTH = 1000


@dataclass
class JournalEntry:
    title: str
    content: str
    tags: list[str] = field(default_factory=list)
    date: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        if not self.title or len(self.title) > MAX_TITLE_LENGTH:
            raise ValueError(f"Title must be non-empty and <= {MAX_TITLE_LENGTH} characters")
        if not self.content or len(self.content) > MAX_CONTENT_LENGTH:
            raise ValueError(f"Content must be non-empty and <= {MAX_CONTENT_LENGTH} characters")


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


def main():
    print("Hello from dev-journal!")


if __name__ == "__main__":
    main()
