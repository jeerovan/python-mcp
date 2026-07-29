# Architecture

## Overview

Python Intelligence MCP Server introspects Python environments and exposes findings as MCP tools for AI agents.

```
┌─────────────────────────────────────────────────────┐
│                   MCP Client (Agent)                │
└────────────────────────┬────────────────────────────┘
                         │ stdio
┌────────────────────────▼────────────────────────────┐
│              src/server.py (FastMCP)                 │
│   Tool registration + request dispatch              │
└────────────────────────┬────────────────────────────┘
                         │
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
┌──────────┐    ┌──────────────┐   ┌──────────────┐
│ Cache    │    │ Inspectors   │   │ Models       │
│ (env)    │    │ (10 modules) │   │ (responses)  │
└──────────┘    └──────────────┘   └──────────────┘
```

## Layers

### 1. Server (`src/server.py`)
FastMCP entry point. Registers tools, delegates to inspectors.

### 2. Inspectors (`src/inspectors/`)
Static-method classes, one per concern. No shared state.

| Inspector | Responsibility |
|-----------|---------------|
| `EnvironmentInspector` | Interpreter, paths, env vars |
| `PackageInspector` | Distributions, metadata, docs |
| `ModuleInspector` | Module-level symbols |
| `ClassInspector` | Class structure, MRO, resolve |
| `FunctionInspector` | Signatures, parameters |
| `SourceInspector` | Source retrieval |
| `DependencyInspector` | Import graph (NetworkX) |
| `SymbolSearchInspector` | AST-based symbol search |
| `ImportResolver` | `importlib` path resolution |
| `TypeHierarchyInspector` | Inheritance hierarchy |
| `StubInspector` | `.pyi` file reading |
| `EnvironmentComparator` | Env diffing |
| `DocumentationInspector` | pydoc + TF semantic search |

### 3. Cache (`src/cache/`)
Environment-keyed cache. Reduces repeated introspection cost.

### 4. Models (`src/models/`)
Pydantic response models: `MCPResponse`, `ErrorDetails`.

## Data Flow

1. Client calls tool via MCP
2. `server.py` tool function invoked
3. Inspector static method executes
4. Inspector may use `global_cache` for env-scoped results
5. Result returned as dict → serialized by FastMCP

## Key Design Decisions

- **Static methods**: Inspectors stateless. Easy testing, no lifecycle mgmt.
- **Lazy imports**: Phase 2+ inspectors imported inside tool functions originally; now top-level for clarity.
- **`_resolve_object`**: ClassInspector walks dotted name greedily, handles nested attrs.
- **AST over regex**: Symbol search uses `ast.parse` — accurate, handles edge cases.
- **TF similarity**: Semantic search uses term-frequency cosine similarity. Lightweight, no external embeddings dependency. Suitable for offline/local use.

## Dependencies

| Package | Purpose |
|---------|---------|
| `mcp` (<2.0) | MCP server framework (FastMCP) |
| `pydantic` | Response models |
| `networkx` | Dependency graphs |
| `packaging` | Version parsing |

## Testing

- `tests/test_inspectors.py` — Phase 1
- `tests/test_phase2.py` — Phase 2
- `tests/test_phase3.py` — Phase 3

Run: `python -m pytest tests/ -v`
