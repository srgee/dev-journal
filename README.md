# dev-journal

A command-line developer journal and logging utility built with Python and Typer.

This project provides a simple, yet effective, way to record and retrieve journal entries from the command line. It allows users to add entries with titles, content, and tags, and then search or list these entries. This tool is useful for developers who want to keep a structured log of their thoughts, progress, or important information encountered during their work.

## Tech Stack

* Python 3.14
* Typer
* uv (for building and dependency management)
* Ruff (for linting and formatting)
* Pre-commit
* Pytest (for testing)
* Betterleaks

## Quick Start

To install and run the `dev-journal` command-line utility:

1. **Clone repo:**
 ```bash
 git clone https://github.com/srgee/dev-journal.git
 ```

1. **Run:**
 The primary command is `journal`. Use `journal --help` for a full list of commands and options.

 * **Add an entry:**
 ```bash
 uv run journal add --title "My First Entry" --content "This is the content of my first journal entry." --tags "python,testing"
 ```
 You will be prompted for title, content, and tags if not provided as options.

 * **List entries:**
 ```bash
 uv run journal list
 ```
 You can filter by tags or limit the number of entries shown:
 ```bash
 uv run journal list --tags python --limit 5
 ```

 * **Search entries:**
 ```bash
 uv run journal search "keyword"
 ```

See the project manifest (`pyproject.toml`) for detailed dependency information.

## Project Structure

```
.
├── .github/
│ ├── workflows/
│ │ └── ci.yml
│ └── dependabot.yml
├── src/
│ └── journal/
│ ├── __init__.py
│ ├── cli.py
│ ├── db.py
│ ├── __main__.py
│ └── models.py
├── tests/
│ ├── __init__.py
│ ├── conftest.py
│ ├── test_cli.py
│ ├── test_db.py
│ └── test_models.py
├── .betterleaks.toml
├── .pre-commit-config.yaml
├── .python-version
├── pyproject.toml
└── README.md
```

## Key Concepts

* **`src/journal/db.py`**: This module handles all interactions with the journal's data storage. It defines the `JournalDatabase` class, responsible for loading entries from and saving entries to a JSON file, as well as adding new entries and searching existing ones.
* **`src/journal/cli.py`**: This module defines the command-line interface using Typer. It exposes commands like `add`, `list`, and `search`, orchestrating the user interaction and calling the appropriate methods from the `JournalDatabase`.
* **`src/journal/models.py`**: This module defines the data structure for a journal entry. The `JournalEntry` dataclass includes fields for `title`, `content`, `tags`, and `date`, along with validation for title and content length.
* **`pyproject.toml`**: This file serves as the central configuration for the project, defining metadata, dependencies, build system requirements, and tool configurations for linters (Ruff) and test runners (pytest).
* **`tests/`**: This directory contains all the unit and integration tests for the project, ensuring the functionality of the database, CLI, and models.

## License

This project is licensed under the MIT License.