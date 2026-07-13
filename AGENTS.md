# AGENTS.md

## Project

Python project for testing OpenCode agent capabilities.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

## Common Commands

```bash
# Run all tests
pytest

# Run single test file
pytest tests/test_example.py

# Run single test
pytest tests/test_example.py::test_name -v

# Lint + format
ruff check .
ruff format .

# Type check
mypy .

# Run all checks in order
ruff check . && ruff format . && mypy . && pytest
```

## Conventions

- Use `src/` layout (`src/<package_name>/`)
- Tests mirror source structure in `tests/`
- Prefer `ruff` for linting and formatting (replaces black, isort, flake8)
- Use type hints; `mypy` strict mode is on
- Keep functions small and testable
- Name test files `test_<module>.py`, test functions `test_<behavior>`
