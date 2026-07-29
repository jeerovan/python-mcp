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

if __name__ == "__main__":
    mcp.run()
