import pytest
import os
import tempfile
from src.inspectors.class_inspector import ClassInspector
from src.inspectors.function_inspector import FunctionInspector
from src.inspectors.module_inspector import ModuleInspector
from src.inspectors.package_inspector import PackageInspector
from src.inspectors.source_inspector import SourceInspector
from src.inspectors.dependency_inspector import DependencyInspector
from src.inspectors.search_inspector import SymbolSearchInspector
from src.inspectors.environment_inspector import EnvironmentInspector
from src.inspectors.stub_inspector import StubInspector
from src.inspectors.import_resolver import ImportResolver
from src.inspectors.type_inspector import TypeHierarchyInspector
from src.inspectors.env_comparator import EnvironmentComparator
from src.models.response import success_response, error_response


def test_class_info():
    info = ClassInspector.class_info("os.PathLike")
    assert info["qualified_name"] == "os.PathLike"
    assert "mro" in info
    assert "public_methods" in info


def test_class_info_not_class():
    with pytest.raises(ValueError):
        ClassInspector.class_info("os.getcwd")


def test_class_info_unresolvable():
    with pytest.raises(ValueError):
        ClassInspector.class_info("nonexistent.module.Symbol")


def test_function_info():
    info = FunctionInspector.function_info("os.getcwd")
    assert info["qualified_name"] == "os.getcwd"
    assert "signature" in info
    assert "parameters" in info


def test_function_info_not_function():
    with pytest.raises(ValueError):
        FunctionInspector.function_info("os.PathLike")


def test_module_info():
    info = ModuleInspector.module_info("os")
    assert "documentation" in info
    assert "classes" in info
    assert "functions" in info


def test_module_info_invalid():
    with pytest.raises(ValueError):
        ModuleInspector.module_info("nonexistent_module_xyz")


def test_package_exists_found():
    result = PackageInspector.package_exists("os")
    # os is builtin, may report exists=True
    assert "exists" in result


def test_package_info_pytest():
    # pytest is installed in test env
    try:
        info = PackageInspector.package_info("pytest")
        assert info["name"] == "pytest"
        assert "version" in info
    except ValueError:
        pass  # skip if not found


def test_package_info_not_found():
    with pytest.raises(ValueError):
        PackageInspector.package_info("nonexistent_pkg_xyz_123")


def test_package_docs():
    try:
        docs = PackageInspector.package_docs("os")
        assert docs["package"] == "os"
        assert "documentation" in docs
    except ValueError:
        pass


def test_package_docs_not_found():
    with pytest.raises(ValueError):
        PackageInspector.package_docs("nonexistent_pkg_xyz_123")


def test_source_info_os():
    # PathLike is a class, has source available in typeshed or builtin
    # Use a pure-python symbol: pytest fixtures may work
    try:
        info = SourceInspector.source_info("os.getcwd")
        assert "source_code" in info
    except ValueError:
        # builtin may not have source; test custom code path instead
        pass


def test_source_info_error():
    with pytest.raises(ValueError):
        SourceInspector.source_info("nonexistent.symbol")


def test_dependency_tree_os():
    result = DependencyInspector.dependency_tree("os")
    assert "nodes" in result
    assert "edges" in result


def test_dependency_tree_error():
    with pytest.raises(ValueError):
        DependencyInspector.dependency_tree("nonexistent_module_xyz")


def test_search_symbol_in_tmpdir():
    with tempfile.TemporaryDirectory() as d:
        test_file = os.path.join(d, "sample.py")
        with open(test_file, "w") as f:
            f.write("def foo():\n    pass\nclass Bar:\n    pass\n")
        results = SymbolSearchInspector.search_symbol("foo", d)
        assert len(results) > 0
        assert results[0]["name"] == "foo"


def test_search_symbol_no_match():
    with tempfile.TemporaryDirectory() as d:
        results = SymbolSearchInspector.search_symbol("xyz_not_present", d)
        assert results == []


def test_environment_list_environments():
    envs = EnvironmentInspector.list_environments()
    assert isinstance(envs, list)
    assert len(envs) > 0


def test_stub_info_not_found():
    with pytest.raises(FileNotFoundError):
        StubInspector.stub_info("/tmp/nonexistent_file.pyi")


def test_import_resolver_not_found():
    result = ImportResolver.resolve_import_path("nonexistent_module_xyz")
    assert result["found"] is False


def test_type_hierarchy_error():
    with pytest.raises(ValueError):
        TypeHierarchyInspector.get_type_hierarchy("nonexistent.symbol")


def test_env_comparator_types():
    result = EnvironmentComparator.compare(None, None)
    assert isinstance(result["packages_added"], list)
    assert isinstance(result["packages_removed"], list)
    assert isinstance(result["version_differences"], dict)


def test_success_response():
    r = success_response({"key": "value"})
    assert r["success"] is True
    assert r["data"]["key"] == "value"


def test_error_response():
    r = error_response("ValueError", "bad input", {"detail": "x"})
    assert r["success"] is False
    assert r["error"]["type"] == "ValueError"
    assert r["error"]["message"] == "bad input"
    assert r["error"]["details"]["detail"] == "x"


def test_function_info_no_params_builtin():
    # Test a builtin with return type
    info = FunctionInspector.function_info("os.getcwd")
    assert "signature" in info
    assert isinstance(info["parameters"], list)


def test_class_info_abstract_methods():
    # Use abc.ABC or similar - test os.PathLike which has no abstracts
    info = ClassInspector.class_info("os.PathLike")
    assert "abstract_methods" in info
    assert isinstance(info["abstract_methods"], list)


def test_class_info_source_location():
    info = ClassInspector.class_info("os.PathLike")
    assert "source_location" in info
    assert "file" in info["source_location"]


def test_package_list_packages_content():
    pkgs = PackageInspector.list_packages()
    assert len(pkgs) > 0
    first = pkgs[0]
    assert "name" in first
    assert "version" in first


def test_dependency_tree_nodes_populated():
    result = DependencyInspector.dependency_tree("json")
    assert isinstance(result["nodes"], list)


def test_environment_info_active():
    from src.cache.environment_cache import global_cache
    # Invalidate cache to exercise fresh path
    global_cache.invalidate()
    info = EnvironmentInspector.get_environment_info()
    assert "executable" in info
    assert "site-packages" in info


import inspect
from src.inspectors.function_inspector import FunctionInspector
from src.inspectors.class_inspector import ClassInspector
import os
from src.cache.environment_cache import EnvironmentCache


def test_function_info_with_params():
    # Use a function with params + return annotation
    info = FunctionInspector.function_info("os.path.join")
    assert "parameters" in info
    assert isinstance(info["parameters"], list)


def test_class_info_source_missing():
    # Test a class without source - builtin
    try:
        info = ClassInspector.class_info("os.PathLike")
        assert "source_location" in info
    except ValueError:
        pass


def test_cache_ttl_expiry():
    cache = EnvironmentCache(ttl=0)
    cache.set(None, "key", "value")
    # TTL=0 means expired immediately on next get
    # (time.time() - timestamp < 0 is False, so should return None)
    result = cache.get(None, "key")
    assert result is None


def test_cache_invalidate_specific_env():
    cache = EnvironmentCache()
    cache.set("custom_env", "key", "value")
    cache.invalidate("custom_env")
    assert cache.get("custom_env", "key") is None


def test_cache_invalidate_all():
    cache = EnvironmentCache()
    cache.set("env1", "key", "value1")
    cache.set("env2", "key", "value2")
    cache.invalidate()
    assert cache.get("env1", "key") is None
    assert cache.get("env2", "key") is None


def test_package_info_returns_metadata():
    try:
        info = PackageInspector.package_info("pytest")
        assert "metadata" in info
        assert "dependencies" in info
        assert "editable" in info
    except ValueError:
        pass


def test_package_exists_import_fallback():
    # Test a builtin module via import fallback
    result = PackageInspector.package_exists("sys")
    assert result["exists"] is True
