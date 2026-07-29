import os
import tempfile
from src.inspectors.stub_inspector import StubInspector
from src.inspectors.env_comparator import EnvironmentComparator
from src.inspectors.doc_inspector import DocumentationInspector

def test_stub_info_valid():
    with tempfile.NamedTemporaryFile(suffix=".pyi", mode="w", delete=False) as f:
        f.write("def foo(x: int) -> str: ...")
        path = f.name
    try:
        result = StubInspector.stub_info(path)
        assert result["content"] == "def foo(x: int) -> str: ..."
        assert result["size"] > 0
    finally:
        os.remove(path)

def test_stub_info_invalid_extension():
    try:
        StubInspector.stub_info("/tmp/not_stub.py")
        assert False, "Should raise ValueError"
    except ValueError:
        pass

def test_compare_environments():
    result = EnvironmentComparator.compare(None, None)
    assert "version_mismatch" in result
    assert "packages_added" in result
    assert "packages_removed" in result
    assert "version_differences" in result

def test_search_docs():
    result = DocumentationInspector.search_docs("os")
    assert result["query"] == "os"
    assert "documentation" in result or "error" in result

def test_semantic_search():
    result = DocumentationInspector.semantic_search("path handling", top_k=2)
    assert result["query"] == "path handling"
    assert "results" in result
    assert len(result["results"]) <= 2
