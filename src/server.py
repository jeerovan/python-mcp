"""Python Intelligence MCP server.

Exposes Python-environment introspection tools over the Model Context
Protocol (stdio transport). Run with ``python -m src.server``.
"""
import os
import signal
import sys
import threading
import time

from mcp.server.fastmcp import FastMCP
from src.inspectors.environment_inspector import EnvironmentInspector
from src.inspectors.package_inspector import PackageInspector
from src.inspectors.module_inspector import ModuleInspector
from src.inspectors.class_inspector import ClassInspector
from src.inspectors.function_inspector import FunctionInspector
from src.inspectors.source_inspector import SourceInspector
from src.inspectors.dependency_inspector import DependencyInspector
from src.inspectors.search_inspector import SymbolSearchInspector
from src.inspectors.import_resolver import ImportResolver
from src.inspectors.type_inspector import TypeHierarchyInspector
from src.inspectors.stub_inspector import StubInspector
from src.inspectors.env_comparator import EnvironmentComparator
from src.inspectors.doc_inspector import DocumentationInspector

mcp = FastMCP("PythonIntelligence")

# Environment Tools
@mcp.tool()
def get_environment_info(environment: str | None = None):
    """Get detailed info about Python environment."""
    return EnvironmentInspector.get_environment_info(environment)

@mcp.tool()
def list_environments():
    """List detected Python environments."""
    return EnvironmentInspector.list_environments()

# Package Tools
@mcp.tool()
def list_packages(environment: str | None = None):
    """List installed packages."""
    return PackageInspector.list_packages(environment)

@mcp.tool()
def package_info(package_name: str, environment: str | None = None):
    """Get package details."""
    return PackageInspector.package_info(package_name, environment)

@mcp.tool()
def package_docs(package_name: str, environment: str | None = None):
    """Get package documentation."""
    return PackageInspector.package_docs(package_name, environment)

# Module/Class/Function Tools
@mcp.tool()
def module_info(module_name: str, environment: str | None = None):
    """Get module structure."""
    return ModuleInspector.module_info(module_name, environment)

@mcp.tool()
def class_info(qualified_name: str, environment: str | None = None):
    """Get class details."""
    return ClassInspector.class_info(qualified_name, environment)

@mcp.tool()
def function_info(qualified_name: str, environment: str | None = None):
    """Get function details."""
    return FunctionInspector.function_info(qualified_name, environment)

# Phase 2 Tools
@mcp.tool()
def source_info(qualified_name: str, environment: str | None = None):
    """Get source code of symbol."""
    return SourceInspector.source_info(qualified_name, environment)

@mcp.tool()
def dependency_tree(module_name: str, environment: str | None = None):
    """Get dependency tree of a module."""
    return DependencyInspector.dependency_tree(module_name, environment)

@mcp.tool()
def search_symbol(name_pattern: str, search_path: str | None = None):
    """Search for symbols by pattern."""
    return SymbolSearchInspector.search_symbol(name_pattern, search_path)

@mcp.tool()
def import_path(import_path: str):
    """Resolve import path to location."""
    return ImportResolver.resolve_import_path(import_path)

@mcp.tool()
def type_hierarchy(qualified_name: str, environment: str | None = None):
    """Get type hierarchy of a class."""
    return TypeHierarchyInspector.get_type_hierarchy(qualified_name, environment)

# Phase 3 Tools
@mcp.tool()
def stub_info(file_path: str):
    """Get content of .pyi stub file."""
    return StubInspector.stub_info(file_path)

@mcp.tool()
def compare_environments(env1: str, env2: str):
    """Compare two environments."""
    return EnvironmentComparator.compare(env1, env2)

@mcp.tool()
def search_docs(query: str):
    """Search for documentation."""
    return DocumentationInspector.search_docs(query)

@mcp.tool()
def semantic_search(query: str, top_k: int = 5):
    """Semantic search over documentation."""
    return DocumentationInspector.semantic_search(query, top_k)

# --- Lifecycle / graceful shutdown -----------------------------------------
#
# The MCP stdio transport blocks on a stdin read that runs inside an anyio
# worker thread. That read is *not* abandonable on cancellation, so when a
# termination signal arrives before stdin reaches EOF (e.g. Ctrl-C in a
# terminal, or a client that signals the process instead of closing the pipe),
# an ordinary KeyboardInterrupt would wedge the event loop forever.
#
# Strategy: on SIGINT/SIGTERM give the normal shutdown path a brief chance to
# run (which is all that is needed when the peer also closes stdin, and lets
# pending stdout drain), then force a clean exit so the process can never be
# left hanging. The environment cache holds no OS resources, so a forced exit
# is safe here. A second signal exits immediately.

_SHUTDOWN_TIMEOUT = float(os.environ.get("PYTHON_MCP_SHUTDOWN_TIMEOUT", "1.5"))
_shutdown_started = threading.Event()


def _request_shutdown(_signum: int, _frame) -> None:
    """Signal handler: trigger a clean shutdown, forcing exit if it stalls."""
    if _shutdown_started.is_set():
        # A second signal means "exit now".
        os._exit(0)
    _shutdown_started.set()

    def _watchdog() -> None:
        time.sleep(_SHUTDOWN_TIMEOUT)
        for stream in (sys.stdout, sys.stderr):
            try:
                stream.flush()
            except Exception:
                pass
        os._exit(0)

    threading.Thread(
        target=_watchdog, daemon=True, name="mcp-shutdown-watchdog"
    ).start()


def _install_signal_handlers() -> None:
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(sig, _request_shutdown)
        except (ValueError, OSError):
            # Signal handlers can only be registered from the main thread.
            pass
    if hasattr(signal, "SIGPIPE"):
        try:
            signal.signal(signal.SIGPIPE, signal.SIG_IGN)
        except (ValueError, OSError):
            pass


def main() -> None:
    _install_signal_handlers()
    try:
        mcp.run()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        for stream in (sys.stdout, sys.stderr):
            try:
                stream.flush()
            except Exception:
                pass


if __name__ == "__main__":
    main()
