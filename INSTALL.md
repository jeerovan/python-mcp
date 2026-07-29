# Installation

## Prerequisites

- Python 3.10+
- pip

## Install

```bash
git clone <repo-url>
cd python-mcp
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Run Server (stdio)

```bash
python -m src.server
```

## Configure Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "python-intelligence": {
      "command": "python",
      "args": ["-m", "src.server"]
    }
  }
}
```

## Verify

```bash
python -m pytest tests/
```

## Troubleshooting

- `ModuleNotFoundError: mcp.server.fastmcp` → MCP v2.0 removed fastmcp. Pin `mcp<2.0`: `pip install 'mcp<2.0'`
- Python 3.11+ required for `str | None` type syntax
