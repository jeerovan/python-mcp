import inspect
import importlib
from typing import Any, Dict, List, Optional


class ClassInspector:
    @staticmethod
    def _resolve_object(qualified_name: str) -> Any:
        parts = qualified_name.split(".")
        for i in range(len(parts), 0, -1):
            mod_name = ".".join(parts[:i])
            attr_path = parts[i:]
            try:
                mod = importlib.import_module(mod_name)
                obj = mod
                for attr in attr_path:
                    obj = getattr(obj, attr)
                return obj
            except (ImportError, AttributeError):
                continue
        raise ValueError(f"Could not resolve symbol '{qualified_name}'")

    @staticmethod
    def class_info(qualified_name: str, environment: Optional[str] = None) -> Dict[str, Any]:
        cls = ClassInspector._resolve_object(qualified_name)
        if not inspect.isclass(cls):
            raise ValueError(f"Symbol '{qualified_name}' is not a class")

        doc = inspect.getdoc(cls)
        
        constructor_sig = ""
        try:
            constructor_sig = str(inspect.signature(cls.__init__)) if hasattr(cls, "__init__") else ""
        except Exception:
            pass

        bases = [b.__name__ for b in cls.__bases__]
        mro = [c.__name__ for c in cls.__mro__]

        methods = {}
        properties = {}
        abstract_methods = getattr(cls, "__abstractmethods__", set())

        for name, member in inspect.getmembers(cls):
            if name.startswith("_") and name not in ("__init__", "__call__"):
                continue
            if inspect.isfunction(member) or inspect.ismethod(member):
                try:
                    sig = str(inspect.signature(member))
                except Exception:
                    sig = "()"
                methods[name] = {
                    "signature": sig,
                    "documentation": inspect.getdoc(member) or ""
                }
            elif isinstance(member, property):
                properties[name] = {
                    "documentation": inspect.getdoc(member.fget) or ""
                }

        source_file = None
        start_line = None
        end_line = None
        try:
            source_file = inspect.getsourcefile(cls)
            _, start_line = inspect.getsourcelines(cls)
            end_line = start_line + len(inspect.getsource(cls).splitlines()) - 1
        except Exception:
            pass

        return {
            "qualified_name": qualified_name,
            "documentation": doc,
            "constructor_signature": constructor_sig,
            "inheritance": bases,
            "mro": mro,
            "module": cls.__module__,
            "source_location": {
                "file": source_file,
                "start_line": start_line,
                "end_line": end_line
            },
            "public_methods": methods,
            "properties": properties,
            "abstract_methods": list(abstract_methods),
        }

    @staticmethod
    def type_hierarchy(qualified_name: str, environment: Optional[str] = None) -> Dict[str, Any]:
        cls = ClassInspector._resolve_object(qualified_name)
        if not inspect.isclass(cls):
            raise ValueError(f"Symbol '{qualified_name}' is not a class")

        subclasses = [sub.__name__ for sub in cls.__subclasses__()]
        return {
            "class": qualified_name,
            "base_classes": [b.__name__ for b in cls.__bases__],
            "subclasses": subclasses,
            "mro": [c.__name__ for c in cls.__mro__],
        }
