import inspect
import importlib
from typing import Any, Dict, List, Optional
from src.inspectors.class_inspector import ClassInspector


class FunctionInspector:
    @staticmethod
    def function_info(qualified_name: str, environment: Optional[str] = None) -> Dict[str, Any]:
        func = ClassInspector._resolve_object(qualified_name)
        if not (inspect.isfunction(func) or inspect.ismethod(func) or inspect.isbuiltin(func)):
            raise ValueError(f"Symbol '{qualified_name}' is not a function or method")

        try:
            sig = inspect.signature(func)
        except Exception:
            sig = None

        parameters = []
        if sig:
            for p_name, param in sig.parameters.items():
                default_val = None if param.default is inspect.Parameter.empty else param.default
                annotation = None if param.annotation is inspect.Parameter.empty else str(param.annotation)
                parameters.append({
                    "name": p_name,
                    "kind": str(param.kind),
                    "default": str(default_val) if default_val is not None else None,
                    "annotation": annotation
                })

        return_type = None
        if sig and sig.return_annotation is not inspect.Parameter.empty:
            return_type = str(sig.return_annotation)

        doc = inspect.getdoc(func) or ""
        
        source_file = None
        start_line = None
        end_line = None
        try:
            source_file = inspect.getsourcefile(func)
            _, start_line = inspect.getsourcelines(func)
            end_line = start_line + len(inspect.getsource(func).splitlines()) - 1
        except Exception:
            pass

        return {
            "qualified_name": qualified_name,
            "signature": str(sig) if sig else "()",
            "parameters": parameters,
            "return_type": return_type,
            "documentation": doc,
            "source_location": {
                "file": source_file,
                "start_line": start_line,
                "end_line": end_line
            }
        }
