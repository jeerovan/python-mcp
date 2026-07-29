from typing import Any, Dict, List
from src.inspectors.environment_inspector import EnvironmentInspector
from src.inspectors.package_inspector import PackageInspector

class EnvironmentComparator:
    @staticmethod
    def compare(env1: str, env2: str) -> Dict[str, Any]:
        """Compares two environments."""
        info1 = EnvironmentInspector.get_environment_info(env1)
        info2 = EnvironmentInspector.get_environment_info(env2)
        pkgs1 = {p["name"]: p["version"] for p in PackageInspector.list_packages(env1)}
        pkgs2 = {p["name"]: p["version"] for p in PackageInspector.list_packages(env2)}
        
        diff = {
            "version_mismatch": info1["version"] != info2["version"],
            "packages_added": [p for p in pkgs2 if p not in pkgs1],
            "packages_removed": [p for p in pkgs1 if p not in pkgs2],
            "version_differences": {p: (pkgs1[p], pkgs2[p]) for p in pkgs1 if p in pkgs2 and pkgs1[p] != pkgs2[p]}
        }
        return diff
