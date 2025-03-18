# trello-cli-trec Development Guide

## Development Commands
```bash
# Install dependencies
pipenv install

# Install in development mode
pip install -e .

# Run the application
python -m trec.main

# Clean/rebuild database (no command found)
```

## Code Style Guidelines

### Python Style
- Use Python 3.11+ features
- Typing: Use type hints from `typing` module for function parameters and return values
- Error handling: Raise `ValueError` for invalid inputs with descriptive messages

### Naming Conventions
- Functions: `snake_case` (e.g., `query_for_list`)
- Variables: `snake_case`
- Module names: lowercase, no underscores
- Command methods: Use `name()`, `help()`, `implement()`, `process()` pattern

### Imports
- Standard library imports first
- Third-party imports second
- Application imports third (e.g., `import trec.api as api`)
- Relative imports when appropriate

### API Design
- Command pattern for CLI subcommands
- Each command module implements standard interface with name/help/implement/process
- Consistent error handling with descriptive messages
