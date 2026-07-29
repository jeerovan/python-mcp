# Python Intelligence MCP Server

**Version:** 2.0
**Status:** Final Specification

---

# Vision

Develop a production-quality **Model Context Protocol (MCP) server** that exposes a Python environment as a structured intelligence service for AI coding agents.

Instead of relying on assumptions, outdated training data, or internet searches, AI agents should be able to accurately inspect the user's installed Python environment and retrieve package metadata, documentation, APIs, symbols, source locations, dependency relationships, and type information.

The server should function as a **Python Environment Intelligence API**, enabling AI agents to work confidently with the exact packages installed in a project.

The design must be modular and extensible so that additional language adapters (Node.js, Java, Kotlin, Rust, Go, .NET, etc.) can be added later without changing the MCP protocol.

---

# Goals

The server should allow AI agents to answer questions such as:

* Which Python interpreter is being used?
* Which virtual environment belongs to this project?
* Which packages are installed?
* Is a specific package installed?
* Which version is installed?
* Where is the package located?
* Which modules does it export?
* Which classes exist?
* Which functions exist?
* What are their signatures?
* What are the available overloads?
* What are the type annotations?
* Show documentation.
* Show examples.
* Show inheritance hierarchy.
* Show dependencies.
* Locate the source file.
* Find where a symbol is defined.
* Search documentation using natural language.
* Compare two environments.
* Build a graph of package relationships.

---

# Non Goals

The server is **NOT**

* a Python REPL
* a package installer
* a package updater
* a package remover
* a code execution engine
* a linter
* a formatter
* a test runner
* a debugger

Its responsibility is **inspection and intelligence only**.

---

# Supported Environments

The server must support:

* CPython
* PyPy
* Conda
* venv
* virtualenv
* Poetry
* uv
* Pipenv
* pyenv
* Embedded Python

---

# Virtual Environment Support

Every tool must support inspecting either

* the current interpreter
* a Python executable
* a virtual environment directory

Examples

```
.venv

/home/user/project/.venv

C:\Projects\App\.venv

/usr/bin/python3
```

Every MCP tool should accept an optional parameter:

```json
{
  "environment": "/path/to/.venv"
}
```

If omitted, the active interpreter is used.

The server must maintain independent caches for every environment.

---

# High-Level Architecture

```
AI Agent
      │
      ▼
Python Intelligence MCP Server
      │
      ▼
Inspection Layer
      │
      ├── Environment Inspector
      ├── Package Inspector
      ├── Module Inspector
      ├── Symbol Inspector
      ├── Documentation Inspector
      ├── Dependency Inspector
      ├── Source Inspector
      ├── Type Inspector
      └── Search Engine
      │
      ▼
Python Runtime
      │
      ▼
Installed Packages
```

---

# Functional Requirements

## 1. Environment Discovery

Return

* executable
* version
* implementation
* architecture
* platform
* prefix
* base prefix
* virtual environment
* site-packages
* user site-packages
* sys.path
* environment variables (Python-related only)

---

## 2. Package Discovery

Return

* package name
* version
* summary
* description
* homepage
* author
* license
* installation path
* metadata
* dependencies
* editable install status

Use

* importlib.metadata
* inspect
* pkgutil

Avoid shell commands whenever possible.

---

## 3. Package Existence

Input

```
package_name
```

Return

* exists
* version
* installation path

---

## 4. Package Documentation

Return

* package documentation
* README
* module documentation
* exported modules
* exported classes
* exported functions
* enums
* constants
* exceptions

---

## 5. Module Inspection

Return

* classes
* functions
* constants
* variables
* enums
* exceptions
* documentation

---

## 6. Class Inspection

Return

* documentation
* constructor
* inheritance
* module
* package
* source location
* public methods
* properties
* annotations
* abstract methods
* protocols
* MRO

Every method should include

* signature
* documentation

---

## 7. Function Inspection

Return

* signature
* overloads
* annotations
* parameters
* default values
* return type
* documentation
* examples
* source location

---

## 8. Symbol Search

Support searching

* class
* function
* method
* constant
* enum
* exception

Example

```
DataFrame
```

Return

```
pandas.DataFrame
polars.DataFrame
modin.DataFrame
```

---

## 9. Documentation Search

Search

* docstrings
* README
* API descriptions

Support natural language queries.

Example

```
How do I parse YAML?
```

---

## 10. Import Resolution

Return canonical imports.

Example

```
DataFrame
```

↓

```
import pandas as pd

pd.DataFrame
```

---

## 11. Signature Resolution

Return complete signatures.

Example

```
numpy.mean(
    a,
    axis=None,
    dtype=None,
    out=None,
    keepdims=False
)
```

---

## 12. Example Extraction

Extract examples from

* docstrings
* README
* package documentation

---

## 13. Dependency Graph

Return dependency trees.

Example

```
FastAPI
    └── Starlette
            └── AnyIO
                    └── sniffio
```

---

## 14. Source Navigation

Return

* module
* package
* source file
* relative path
* absolute path
* start line
* end line

---

## 15. Type Hierarchy

Return

* base classes
* subclasses
* MRO
* Protocols
* Abstract classes

---

## 16. Package Symbol Index

Build a searchable index containing

* packages
* modules
* classes
* methods
* functions
* enums
* constants
* decorators
* exceptions

Support fuzzy search.

Support incremental refresh.

---

## 17. Semantic Documentation Search

Build an optional semantic index using embeddings.

Search

* README
* docstrings
* API documentation

Example

```
open sqlite database

async web server

json validation
```

Embedding provider should be pluggable.

---

## 18. Environment Comparison

Compare two Python environments.

Return

* added packages
* removed packages
* upgraded packages
* downgraded packages
* version conflicts

---

## 19. Stub Inspection

Inspect `.pyi` files when available.

Extract

* overloads
* generic types
* Protocols
* TypedDict
* Literal types

---

## 20. Cross Reference Graph

Generate relationships between

```
Package
 ↓
Module
 ↓
Class
 ↓
Method
```

Include

* imports
* inheritance
* composition
* aliases
* exported symbols
* dependency edges

The graph should support traversal and visualization.

---

# MCP Tools

## Environment

* python.environment
* python.environments

---

## Packages

* python.list_packages
* python.package_exists
* python.package_info
* python.package_docs

---

## Modules

* python.module_info

---

## Symbols

* python.search_symbol
* python.symbol_index

---

## Classes

* python.class_info
* python.type_hierarchy

---

## Functions

* python.function_info

---

## Documentation

* python.search_docs
* python.semantic_search

---

## Imports

* python.import_path

---

## Examples

* python.examples

---

## Dependencies

* python.dependency_tree

---

## Source Navigation

* python.source

---

## Graph

* python.graph

---

## Environment Comparison

* python.compare_environments

---

# Suggested Project Structure

```
src/

    server.py

    tools/

        environment.py
        packages.py
        modules.py
        classes.py
        functions.py
        documentation.py
        search.py
        graph.py
        source.py
        dependencies.py
        comparison.py

    inspectors/

        environment_inspector.py
        package_inspector.py
        module_inspector.py
        class_inspector.py
        function_inspector.py
        source_inspector.py
        dependency_inspector.py
        documentation_inspector.py
        stub_inspector.py

    cache/

    models/

    utils/

tests/

docs/
```

---

# Recommended Libraries

* mcp
* inspect
* importlib
* importlib.metadata
* pkgutil
* pathlib
* pydoc
* ast
* packaging
* networkx
* typing_extensions

Optional

* tree-sitter
* sentence-transformers
* faiss
* rapidfuzz

---

# Performance Goals

Environment discovery

<100 ms

Package lookup

<50 ms

Package list

<200 ms

Function lookup

<50 ms

Class lookup

<50 ms

Documentation lookup

<100 ms

Semantic search

<300 ms

---

# Caching

Cache

* package metadata
* documentation
* symbol index
* dependency graph
* signatures
* source locations

Invalidate automatically when

* interpreter changes
* virtual environment changes
* installed packages change
* package version changes
* site-packages timestamp changes

Maintain separate caches for every environment.

---

# Error Handling

Never expose raw exceptions.

Return structured responses.

Example

```json
{
  "success": false,
  "error": {
    "type": "ModuleNotFound",
    "message": "Package 'numpyx' is not installed.",
    "details": {}
  }
}
```

---

# Logging

Log

* tool name
* execution time
* cache hit/miss
* warnings
* exceptions

Never log source code or user-sensitive information unnecessarily.

---

# Testing

Create automated tests for

* environment detection
* package discovery
* documentation lookup
* source navigation
* dependency graph
* signature extraction
* symbol search
* semantic search
* environment comparison

Target >90% unit test coverage for inspection logic.

---

# Documentation Deliverables

Generate

* README.md
* INSTALL.md
* API.md
* ARCHITECTURE.md
* CHANGELOG.md
* CONTRIBUTING.md

Every MCP tool should include usage examples.

---

# Development Phases

## Phase 1

* Environment discovery
* Package discovery
* Package metadata
* Module inspection
* Class inspection
* Function inspection

## Phase 2

* Source navigation
* Dependency graph
* Symbol search
* Import resolver
* Type hierarchy

## Phase 3

* Symbol indexing
* Semantic documentation search
* Stub inspection
* Environment comparison

## Phase 4

* Cross-reference graph
* Background indexing
* Incremental cache refresh
* IDE integrations
* Performance optimization

## Phase 5

* Language adapter abstraction
* Node.js adapter
* Java adapter
* Go adapter
* Rust adapter
* Kotlin adapter
* .NET adapter

---

# Future Vision

This project is the first implementation of a broader **Environment Intelligence Platform**. Python-specific functionality should remain isolated behind an adapter interface so that future language implementations can reuse the same MCP tool contracts.

The long-term objective is a unified intelligence layer that enables AI agents to inspect and reason about development environments across multiple programming languages without relying on internet access.

---

# Success Criteria

An AI agent should be able to:

* understand any Python environment accurately
* inspect installed packages without assumptions
* discover APIs, symbols, and documentation
* navigate to source code
* resolve imports
* understand type hierarchies
* compare virtual environments
* answer package-related questions entirely from local inspection

without executing arbitrary user code or requiring internet access.

