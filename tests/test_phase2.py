import pytest
from src.inspectors.source_inspector import SourceInspector
from src.inspectors.dependency_inspector import DependencyInspector
from src.inspectors.search_inspector import SymbolSearchInspector
from src.inspectors.import_resolver import ImportResolver
from src.inspectors.type_inspector import TypeHierarchyInspector

def test_source_info():
    info = SourceInspector.source_info("os")
    assert "source_code" in info

def test_import_resolver():
    res = ImportResolver.resolve_import_path("os")
    assert res["found"] is True

def test_type_hierarchy():
    res = TypeHierarchyInspector.get_type_hierarchy("os.PathLike")
    assert "subclasses" in res
