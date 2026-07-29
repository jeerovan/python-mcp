import importlib.metadata
import pkgutil
import inspect
import os
from typing import Any, Dict, List, Optional
from src.cache.environment_cache import global_cache


class PackageInspector:
    @staticmethod
    def list_packages(environment: Optional[str] = None) -> List[Dict[str, Any]]:
        cache_key = "list_packages"
        cached = global_cache.get(environment, cache_key)
        if cached is not None:
            return cached

        packages = []
        try:
            for dist in importlib.metadata.distributions():
                name = dist.metadata.get("Name")
                version = dist.version
                summary = dist.metadata.get("Summary", "")
                packages.append({
                    "name": name,
                    "version": version,
                    "summary": summary,
                })
        except Exception:
            for module_info in pkgutil.iter_modules():
                packages.append({
                    "name": module_info.name,
                    "version": "unknown",
                    "summary": "",
                })

        global_cache.set(environment, cache_key, packages)
        return packages

    @staticmethod
    def package_exists(package_name: str, environment: Optional[str] = None) -> Dict[str, Any]:
        try:
            dist = importlib.metadata.distribution(package_name)
            return {
                "exists": True,
                "name": package_name,
                "version": dist.version,
                "installation_path": str(dist.locate_file(""))
            }
        except Exception:
            try:
                __import__(package_name)
                return {
                    "exists": True,
                    "name": package_name,
                    "version": "unknown",
                    "installation_path": None
                }
            except ImportError:
                return {
                    "exists": False,
                    "name": package_name,
                    "version": None,
                    "installation_path": None
                }

    @staticmethod
    def package_info(package_name: str, environment: Optional[str] = None) -> Dict[str, Any]:
        try:
            dist = importlib.metadata.distribution(package_name)
            metadata = dict(dist.metadata)
            requires = dist.requires or []
            return {
                "name": package_name,
                "version": dist.version,
                "summary": metadata.get("Summary", ""),
                "description": metadata.get("Description", ""),
                "homepage": metadata.get("Home-page", ""),
                "author": metadata.get("Author", ""),
                "license": metadata.get("License", ""),
                "installation_path": str(dist.locate_file("")),
                "metadata": metadata,
                "dependencies": requires,
                "editable": os.path.exists(os.path.join(str(dist.locate_file("")), "setup.py")) or os.path.exists(os.path.join(str(dist.locate_file("")), "pyproject.toml"))
            }
        except Exception as e:
            raise ValueError(f"Package '{package_name}' not found: {str(e)}")

    @staticmethod
    def package_docs(package_name: str, environment: Optional[str] = None) -> Dict[str, Any]:
        try:
            mod = __import__(package_name)
            doc = inspect.getdoc(mod) or ""
            readme = ""
            try:
                dist = importlib.metadata.distribution(package_name)
                # Check for readme in files
                for f in dist.files or []:
                    if "README" in f.name.upper():
                        readme_path = dist.locate_file(f)
                        if os.path.exists(readme_path):
                            with open(readme_path, "r", encoding="utf-8", errors="ignore") as rf:
                                readme = rf.read()
                            break
            except Exception:
                pass

            modules = []
            if hasattr(mod, "__path__"):
                for _, modname, _ in pkgutil.walk_packages(mod.__path__, mod.__name__ + "."):
                    modules.append(modname)

            return {
                "package": package_name,
                "documentation": doc,
                "readme": readme,
                "exported_modules": modules[:50],  # limit sample
            }
        except Exception as e:
            raise ValueError(f"Could not load docs for '{package_name}': {str(e)}")
