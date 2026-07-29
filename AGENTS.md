# Agent Instructions — Python Intelligence MCP Server

This file is loaded by AI coding agents at session start. It defines the coding policy for working in this repository and prescribes which MCP tool to call before each kind of decision. Following these rules keeps the agent's output pinned to the exact installed code, not stale memory.

## Core principle

**Never guess Python facts. Query the server first.** Library APIs drift between versions, agent memory drifts further. Every signature, parameter, import path, and inheritance claim must come from a live tool call, not recall.

## Required context (load once per session)

Call these tools at the start of any Python task. Cache the results mentally so subsequent decisions reference a known environment, not assumptions:

1. `get_environment_info` — active interpreter version, `sys.path`, `site-packages` location. Confirms which Python the agent is writing against.
2. `list_packages` — full installed distribution list. The agent consults this before recommending any `import` so it never suggests a library that is not installed.
3. `import_path("<project.module>")` — confirms the project's own modules resolve. If this fails, the project is not on `sys.path`; run `pip install -e .` or fix `cwd` before writing code.

## Tool selection rules

Map the task to the first tool that resolves it cheapest. Do not call broader tools when a narrower one exists.

| Task | Required tool call | Rationale |
|---|---|---|
| Write or modify an `import` line | `import_path` before writing | Prevents `ModuleNotFoundError` |
| Call a function whose signature is uncertain | `function_info` | Returns exact parameters, defaults, return type |
| Override or extend a class | `class_info` + `type_hierarchy` | Reveals methods, MRO, abstract methods before override |
| Refactor imports across a module | `dependency_tree` | Shows module coupling before edit |
| Recommend an external library | `package_exists` then `package_info` | Confirms installed + reads its dependencies |
| Inspect a `.pyi` type stub | `stub_info` | Aligns runtime code with type-checker contract |
| Find all symbols matching a pattern | `search_symbol` | AST-accurate, returns file + line |
| Compare two environments (dev vs prod) | `compare_environments` | Reveals package/version drift |
| Look up package documentation | `search_docs` | Uses `pydoc.render_doc` on installed code |
| Rank candidates by relevance | `semantic_search` | TF cosine similarity over module docs |

## Coding rules

- **Verify before `import`.** Every new `import` statement must be preceded by an `import_path` call. If unresolved, do not write the import; report the failure.
- **No invented signatures.** When writing a function call, the parameter list must match what `function_info` returned. Defaults and return types come from the tool, not memory.
- **Respect the MRO.** Before adding a method override, call `type_hierarchy` and confirm no parent already declares it with incompatible semantics.
- **Type stubs are authoritative.** If a `.pyi` exists for the module being edited, read it via `stub_info` before touching the `.py`. Runtime code must match the stub's type contracts.
- **Do not recommend uninstalled packages.** Before suggesting `pip install <pkg>`, call `package_exists`. If already present, reference the installed version.
- **State the qualified name.** When inspecting a symbol, pass the full dotted path (`src.inspectors.package_inspector.PackageInspector.list_packages`), not a fragment. Fragments trigger broad `search_symbol` scans that return multiple candidates.

## What the agent should not do

- Do not `"recall"` or `"remember"` library APIs. Tool output is the source of truth.
- Do not write code targeting a Python version different from the active interpreter without stating the target explicitly in the first message.
- Do not assume a virtualenv is active. If `get_environment_info` shows a system prefix rather than a venv, stop and notify the user before writing code.
- Do not run destructive operations (`DROP`, `rm -rf`, `git reset --hard`) without explicit confirmation, even if the user asks.

## Failure handling

If a tool raises `ValueError("Could not resolve symbol ...")` or `ModuleNotFoundError`, the symbol is not importable in the active environment. Do not retry with guesses. Report which symbol failed and what the user must install or activate.

## Testing policy

After any code change:
1. Run `python -m pytest tests/ --cov=src --cov-config=pyproject.toml`.
2. Target: all tests pass, coverage ≥ 90%.
3. If a new inspector or tool is added, add a test in the matching `tests/test_phase<N>.py` before marking the task complete.
