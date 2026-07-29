import pytest
from src.inspectors.environment_inspector import EnvironmentInspector
from src.inspectors.package_inspector import PackageInspector

def test_environment_info():
    info = EnvironmentInspector.get_environment_info()
    assert "version" in info
    assert "sys_path" in info

def test_list_packages():
    pkgs = PackageInspector.list_packages()
    assert isinstance(pkgs, list)
    assert len(pkgs) > 0
