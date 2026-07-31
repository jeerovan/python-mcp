import os
import sys
import platform
from typing import Optional


def run_in_environment(environment: Optional[str], func, *args, **kwargs):
    """
    If environment is provided or a local venv/ .venv exists in the root folder,
    use its site-packages or path for execution.
    """
    root_dir = os.getcwd()
    local_venv = None
    for candidate in (".venv", "venv"):
        candidate_path = os.path.join(root_dir, candidate)
        if os.path.isdir(candidate_path):
            bin_dir = "Scripts" if platform.system() == "Windows" else "bin"
            py_name = "python.exe" if platform.system() == "Windows" else "python"
            if os.path.isfile(os.path.join(candidate_path, bin_dir, py_name)):
                local_venv = candidate_path
                break

    target_env = environment or os.environ.get("VIRTUAL_ENV") or local_venv
    if target_env and os.path.isdir(target_env):
        # Add site-packages of the target_env to sys.path temporarily if not already present
        lib_dir = os.path.join(target_env, "Lib", "site-packages") if platform.system() == "Windows" else os.path.join(target_env, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages")
        if os.path.isdir(lib_dir) and lib_dir not in sys.path:
            sys.path.insert(0, lib_dir)

    return func(*args, **kwargs)
