import inspect
import pkgutil
import importlib
import enum
from typing import Any, Dict, List, Optional


class ModuleInspector:
    @staticmethod
    def module_info(module_name: str, environment: Optional[str] = None) -> Dict[str, Any]:
        try:
            mod = importlib.import_module(module_name)
        except Exception as e:
            raise ValueError(f"Module '{module_name}' could not be imported: {str(e)}")

        classes = []
        functions = []
        constants = []
        variables = []
        enums_list = []
        exceptions = []

        doc = inspect.getdoc(mod)

        for name, obj in inspect.getmembers(mod):
            if name.startswith("_"):
                continue
            if inspect.isclass(obj):
                if issubclass(obj, Exception):
                    exceptions.append(name)
                elif issubclass(obj, enum.Enum):
                    enums_list.append(name)
                else:
                    classes.append(name)
            elif inspect.isfunction(obj) or inspect.isbuiltin(obj):
                functions.append(name)
            elif name.isupper():
                constants.append(name)
            else:
                variables.append(name)

        return {
            "module": module_name,
            "documentation": doc,
            "classes": classes,
            "functions": functions,
            "constants": constants,
            "variables": variables,
            "enums": enums_list,
            "exceptions": exceptions,
        }
