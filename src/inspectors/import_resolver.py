import importlib
import os
import sys
from typing import Any, Dict, Optional

class ImportResolver:
    @staticmethod
    def resolve_import_path(import_path: str) -> Dict[str, Any]:
        """Resolves module import path to file location."""
        try:
            # Use importlib.util.find_spec to locate
            import importlib.util
            spec = importlib.util.find_spec(import_path)
            if spec is None:
                return {"found": False, "path": None}
            
            return {
                "found": True,
                "path": spec.origin,
                "is_package": spec.submodule_search_locations is not None
            }
        except Exception as e:
            return {"found": False, "error": str(e)}
