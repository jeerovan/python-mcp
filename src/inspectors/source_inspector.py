import os
import inspect
import importlib
from typing import Any, Dict, Optional
from src.inspectors.class_inspector import ClassInspector

class SourceInspector:
    @staticmethod
    def source_info(qualified_name: str, environment: Optional[str] = None) -> Dict[str, Any]:
        obj = ClassInspector._resolve_object(qualified_name)
        try:
            source_file = inspect.getsourcefile(obj)
            source_code = inspect.getsource(obj)
            _, start_line = inspect.getsourcelines(obj)
            end_line = start_line + len(source_code.splitlines()) - 1
            
            rel_path = source_file
            if source_file:
                try:
                    rel_path = os.path.relpath(source_file)
                except Exception:
                    pass

            return {
                "qualified_name": qualified_name,
                "module": getattr(obj, "__module__", None),
                "source_file": source_file,
                "relative_path": rel_path,
                "absolute_path": os.path.abspath(source_file) if source_file else None,
                "start_line": start_line,
                "end_line": end_line,
                "source_code": source_code
            }
        except Exception as e:
            raise ValueError(f"Could not retrieve source for '{qualified_name}': {str(e)}")
