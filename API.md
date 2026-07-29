# API Reference

All tools exposed via MCP `tools/list`. Each returns JSON.

## Environment Tools

### `get_environment_info(environment?)`
Returns executable, version, implementation, architecture, prefix, site-packages, sys_path, env vars.

### `list_environments()`
Lists active + detected virtual environments.

## Package Tools

### `list_packages(environment?)`
List all installed distributions (name, version, summary).

### `package_info(package_name, environment?)`
Full metadata: summary, description, homepage, author, license, dependencies, editable flag.

### `package_docs(package_name, environment?)`
Module docstring, README content, exported submodules (up to 50).

## Module/Class/Function Tools

### `module_info(module_name, environment?)`
Module doc, classes, functions, constants, variables, enums, exceptions.

### `class_info(qualified_name, environment?)`
Doc, constructor signature, inheritance, MRO, public methods (with signatures + docs), properties, abstract methods, source location.

### `function_info(qualified_name, environment?)`
Signature, parameters (name, kind, default, annotation), return type, doc, source location.

## Phase 2 Tools

### `source_info(qualified_name, environment?)`
Source code, module, file paths (relative + absolute), start/end lines.

### `dependency_tree(module_name, environment?)`
NetworkX graph: nodes (modules) + edges (import relationships).

### `search_symbol(name_pattern, search_path?)`
AST-based search. Returns matching functions/classes with file + line.

### `import_path(import_path)`
Resolves import string to file location via `importlib.util.find_spec`.

### `type_hierarchy(qualified_name, environment?)`
Base classes, subclasses, full MRO.

## Phase 3 Tools

### `stub_info(file_path)`
Read `.pyi` stub file content + size.

### `compare_environments(env1, env2)`
Diff: version mismatch flag, packages added/removed, version differences.

### `search_docs(query)`
Render module documentation via `pydoc.render_doc`.

### `semantic_search(query, top_k=5)`
TF cosine similarity ranking over importable module docs. Returns ranked candidates with scores.

## Response Models

Defined in `src/models/response.py`:

- `MCPResponse` — `{success: bool, data?, error?}`
- `ErrorDetails` — `{type, message, details}`
