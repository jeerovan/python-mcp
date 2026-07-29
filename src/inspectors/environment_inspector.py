import os
import platform
import sys
import site
from typing import Any, Dict, List, Optional
from src.cache.environment_cache import global_cache


class EnvironmentInspector:
    @staticmethod
    def get_environment_info(environment: Optional[str] = None) -> Dict[str, Any]:
        cache_key = "environment_info"
        cached = global_cache.get(environment, cache_key)
        if cached is not None:
            return cached

        # If environment is a custom path, determine interpreter / site-packages
        executable = sys.executable
        prefix = sys.prefix
        base_prefix = getattr(sys, "base_prefix", prefix)
        
        venv = os.environ.get("VIRTUAL_ENV") or (prefix if prefix != base_prefix else None)
        
        py_env_vars = {k: v for k, v in os.environ.items() if "PYTHON" in k.upper() or k in ("VIRTUAL_ENV", "CONDA_PREFIX")}

        info = {
            "executable": executable,
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "architecture": platform.architecture()[0],
            "platform": platform.platform(),
            "prefix": prefix,
            "base_prefix": base_prefix,
            "virtual_environment": venv,
            "site-packages": site.getsitepackages() if hasattr(site, "getsitepackages") else [],
            "user_site-packages": site.getusersitepackages() if hasattr(site, "getusersitepackages") else None,
            "sys_path": sys.path,
            "environment_variables": py_env_vars,
        }

        global_cache.set(environment, cache_key, info)
        return info

    @staticmethod
    def list_environments() -> List[Dict[str, Any]]:
        envs = []
        active = EnvironmentInspector.get_environment_info()
        envs.append({
            "name": "active",
            "executable": active["executable"],
            "virtual_environment": active["virtual_environment"]
        })
        venv_env = os.environ.get("VIRTUAL_ENV")
        if venv_env and venv_env != active["virtual_environment"]:
            envs.append({
                "name": "virtual_env",
                "virtual_environment": venv_env
            })
        return envs
