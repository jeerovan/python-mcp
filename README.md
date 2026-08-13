# Python Intelligence MCP Server

Model Context Protocol server providing deep Python environment introspection for AI coding agents.

> **For AI agents:** Read [`AGENTS.md`](AGENTS.md) at session start. It defines the coding policy, required context, and which introspection tool to call before each type of decision (writing imports, overriding methods, recommending packages, etc.).

## Features

- Environment inspection (active + virtual environments)
- Package listing, lookup, metadata, docs
- Module/class/function introspection
- Source code retrieval with line ranges
- Dependency tree analysis (NetworkX graph)
- Symbol search across source trees
- Import path resolution
- Type hierarchy (bases, subclasses, MRO)
- `.pyi` stub inspection
- Environment comparison (diff packages, versions)
- Documentation search + TF-based semantic search

## Quick Start

```bash
git clone <repo-url> && cd python-mcp
python3 -m venv venv && source venv/bin/activate
pip install -e .
python -m src.server
```

## Running from Any Location

Once installed with `pip install -e .`, the package is importable from anywhere — no need to `cd` into the repo. The install also creates a `python-mcp` command that runs the server directly:

```bash
# With the repo's venv active, from any directory:
python-mcp

# Without activating, using the repo venv's absolute path:
/home/pi/developement/python-mcp/venv/bin/python-mcp
/home/pi/developement/python-mcp/venv/bin/python -m src.server
```

### Using a venv located elsewhere

To run the server from a different virtual environment (e.g. `~/myproject/.venv`), install the package into that venv once. It is a pure-Python, source-installable project, so a `--no-deps` editable install is enough when dependencies are already present:

```bash
# From the other project's directory:
~/myproject/.venv/bin/pip install -e /home/pi/developement/python-mcp --no-deps

# Then run it anywhere via that venv:
~/myproject/.venv/bin/python -m src.server
# or, once installed with dependencies:
~/myproject/.venv/bin/python-mcp
```

If you do not want to install the package, `PYTHONPATH` also works:

```bash
PYTHONPATH=/home/pi/developement/python-mcp ~/myproject/.venv/bin/python -m src.server
```

## Integration with AI Agents

The server speaks the Model Context Protocol over stdio. Any MCP-aware agent is a compatible client. The agent invokes tools automatically when a task warrants environment introspection — but only if the client is configured to spawn this server.

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or the equivalent path on other OSes. Use the venv's absolute interpreter path so the server starts regardless of the client's working directory:

```json
{
  "mcpServers": {
    "python-intelligence": {
      "command": "/home/pi/developement/python-mcp/venv/bin/python",
      "args": ["-m", "src.server"]
    }
  }
}
```

Restart Claude Desktop. The server appears in the developer tools panel. The agent can now call any `python.*` tool directly when a request requires Python environment knowledge — no manual prompting required.

### Programmatic Client (Python)

Build a custom agent loop with the official `mcp` SDK on the client side:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(
        command="/home/pi/developement/python-mcp/venv/bin/python",
        args=["-m", "src.server"],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            # Agent chooses tools from this list:
            result = await session.call_tool(
                "module_info",
                {"module_name": "package_inspector"}
            )
            print(result.content)

asyncio.run(main())
```

### VS Code (MCP extension)

Add an entry to `.vscode/mcp.json` in the workspace:

```json
{
  "servers": {
    "python-intelligence": {
      "type": "stdio",
      "command": "/home/pi/developement/python-mcp/venv/bin/python",
      "args": ["-m", "src.server"]
    }
  }
}
```

## Prerequisites for Efficient Python Coding

To trigger effective, low-latency Python coding assistance, expose the following context to the agent before issuing a task. The server provides most of it automatically; the rest is the developer's responsibility.

### Server provides (automatic)

- **Detectable environment** — active interpreter version, virtualenv path, `sys.path`, `site-packages`. Run `get_environment_info` once per session.
- **Installed packages** — full distribution list with versions. The agent uses `list_packages` before suggesting `import` statements so it never recommends an uninstalled library.
- **Symbol resolution** — `class_info`, `function_info`, `source_info` return signatures, parameters, default values, return types, and source line ranges. The agent consults these instead of guessing from memory, so it never invents a parameter that does not exist.
- **Dependency graph** — `dependency_tree` reveals module coupling before the agent refactors imports.
- **Type hierarchy** — `type_hierarchy` exposes base classes, subclasses, and the full MRO so the agent checks inheritance before suggesting overrides or `isinstance` branches.
- **Import paths** — `import_path` confirms whether a module resolves before the agent writes an `import` line; prevents `ModuleNotFoundError` cycles.
- **Stubs** — `stub_info` reads `.pyi` files so the agent can align runtime code with type-checker contracts.
- **Environment comparison** — `compare_environments` diffs two interpreters; the agent avoids suggesting packages present in dev but absent in production.

### Developer provides (required)

1. **Root virtual environment (`.venv` or `venv`).** The server automatically detects a virtual environment folder (`.venv` or `venv`) in the project's root working directory if `VIRTUAL_ENV` is not explicitly set, ensuring project-specific dependencies are inspected correctly.
2. **Project on `sys.path`.** Either install the project (`pip install -e .`) or set `cwd` to the repo root so `import_path` and `module_info` resolve the project's own modules, not a distractor from site-packages.
3. **Concrete target.** State the qualified name when possible: `"inspect function src.inspectors.package_inspector.PackageInspector.list_packages"` beats "look at the package code." Dotted paths trigger one tool call; vague prompts trigger broad `search_symbol` scans that return many candidates.
4. **Version pin.** Tell the agent the target Python version if it differs from the active interpreter (`target: Python 3.10` when venv is 3.14). The server reports the active interpreter, not the deployment target.
5. **Constraints up front.** Declare forbidden dependencies, style rules, or compatibility floors in the first message. The agent does not query for constraints mid-task.

## Triggering the Agent Efficiently

Phrase the task so that the introspection tools are the cheapest path to a correct answer. Good triggers map directly to a tool:

| Task phrasing | Tool the agent should call first |
|---|---|
| "What does `X.function` accept?" | `function_info` |
| "Where is `X` defined?" | `import_path` then `source_info` |
| "What inherits from `X`?" | `type_hierarchy` |
| "Is `package` installed?" | `package_exists` |
| "How do these two environments differ?" | `compare_environments` |
| "Find all classes named `*Handler`" | `search_symbol` |
| "What modules does `X` import?" | `dependency_tree` |

Avoid asking the agent to "recall" or "remember" library APIs — these drift between versions. Pointing the agent at the introspection tools keeps answers pinned to the exact installed code.

## Agent Instructions

The full coding policy — required context to load per session, tool selection rules, coding rules (verify before `import`, no invented signatures, respect the MRO, stubs are authoritative), what the agent must not do, and the testing policy — lives in [`AGENTS.md`](AGENTS.md). MCP-aware clients (Claude Code, Cursor, etc.) load it automatically at session start. For programmatic clients, paste its contents into the system prompt or include it as an initial context resource.

## Usage

Connect any MCP-aware client to this server. All tools are exposed under the `python.*` namespace. See [INSTALL.md](INSTALL.md), [API.md](API.md), [ARCHITECTURE.md](ARCHITECTURE.md).

## License

MIT
