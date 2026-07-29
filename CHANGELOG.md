# Changelog

All notable changes documented here. Format follows [Keep a Changelog](https://keepachangelog.com/).

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
