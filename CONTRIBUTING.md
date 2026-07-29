# Contributing

## Development Setup

```bash
git clone <repo-url>
cd python-mcp
python3 -m venv venv
source venv/bin/activate
pip install -e .
pip install pytest pytest-cov
```

## Code Style

- Python 3.10+
- Type hints required on all public functions
- `str | None` over `Optional[str]`
- Static methods for inspectors (stateless)
- Pydantic models for structured responses

## Project Structure

```
src/
  server.py           # MCP entry point
  cache/              # Caching layer
  inspectors/         # Introspection logic (one file per concern)
  models/             # Pydantic response models
  utils/              # Helpers
tests/                # pytest suites
docs/                 # Documentation
```

## Adding New Tools

1. Create inspector in `src/inspectors/<name>_inspector.py`
2. Add static method returning `Dict[str, Any]`
3. Register `@mcp.tool()` function in `src/server.py`
4. Write tests in `tests/test_phase<N>.py`
5. Update `API.md` and `CHANGELOG.md`

## Testing

```bash
python -m pytest tests/ -v
python -m pytest tests/ --cov=src --cov-report=term-missing
```

Target: >90% coverage.

## Pull Requests

1. Branch from `main`
2. One feature/fix per PR
3. All tests pass
4. Update CHANGELOG
5. Describe "why" not just "what"
