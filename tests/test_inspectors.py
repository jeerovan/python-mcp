import pytest
import os
import tempfile
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

def test_root_venv_detection():
    # Since we created 'venv' in root, EnvironmentInspector should detect it if VIRTUAL_ENV is unset
    old_ve = os.environ.get("VIRTUAL_ENV")
    if "VIRTUAL_ENV" in os.environ:
        del os.environ["VIRTUAL_ENV"]
    try:
        info = EnvironmentInspector.get_environment_info()
        assert info["virtual_environment"] is not None
        assert "venv" in info["virtual_environment"]
    finally:
        if old_ve:
            os.environ["VIRTUAL_ENV"] = old_ve

