# Changelog

All notable changes documented here. Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Fixed
- Server now shuts down cleanly on agent exit and termination signals
  (`SIGINT`/`SIGTERM`). Previously the process could hang forever because the
  MCP stdio transport blocks on a stdin read inside a non-cancellable anyio
  worker thread; a termination signal that arrives before stdin reaches EOF
  wedged the event loop. A main-thread signal handler now gives the normal
  shutdown path a brief window (configurable via `PYTHON_MCP_SHUTDOWN_TIMEOUT`,
  default `1.5`s) and force-exits cleanly afterward, so the process can never
  be left hanging. A second signal exits immediately.

## [2.0.0] - 2025-07-28

### Added
- Environment inspection tools (`get_environment_info`, `list_environments`)
- Package tools (`list_packages`, `package_info`, `package_docs`)
- Module/class/function introspection (`module_info`, `class_info`, `function_info`)
- Source code retrieval (`source_info`)
- Dependency tree analysis via NetworkX (`dependency_tree`)
- AST-based symbol search (`search_symbol`)
- Import path resolution (`import_path`)
- Type hierarchy with MRO (`type_hierarchy`)
- `.pyi` stub inspection (`stub_info`)
- Environment comparison (`compare_environments`)
- Documentation search via pydoc (`search_docs`)
- TF cosine similarity semantic search (`semantic_search`)
- Pydantic response models (`MCPResponse`, `ErrorDetails`)
- Environment-scoped caching layer
- Unit tests for Phases 1-3 (10 tests)
- Documentation: README, INSTALL, API, ARCHITECTURE, CONTRIBUTING, CHANGELOG

### Changed
- Server entry point consolidated with top-level inspector imports

### Fixed
- `server.py` mangled tool registration restored
- MCP version pinned to `<2.0` (fastmcp removed in v2.0)
