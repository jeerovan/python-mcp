import ast
import os
import inspect
from typing import Any, Dict, List, Optional
from src.inspectors.class_inspector import ClassInspector

class SymbolSearchInspector:
    @staticmethod
    def search_symbol(name_pattern: str, search_path: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        path = search_path or os.getcwd()
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r") as f:
                            tree = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                                if name_pattern in node.name:
                                    results.append({
                                        "name": node.name,
                                        "type": type(node).__name__,
                                        "file": full_path,
                                        "line": node.lineno
                                    })
                    except Exception:
                        continue
        return results
