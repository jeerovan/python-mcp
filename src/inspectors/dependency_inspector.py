import networkx as nx
import inspect
import importlib
from typing import Any, Dict, Optional

class DependencyInspector:
    @staticmethod
    def dependency_tree(module_name: str, environment: Optional[str] = None) -> Dict[str, Any]:
        try:
            mod = importlib.import_module(module_name)
        except Exception as e:
            raise ValueError(f"Module '{module_name}' could not be imported: {str(e)}")

        graph = nx.DiGraph()
        
        def _build_deps(m):
            if not hasattr(m, "__file__"):
                return
            
            # Simple heuristic: inspect imports
            # Real impl should parse AST for imports
            for name, obj in inspect.getmembers(m):
                if inspect.ismodule(obj) and hasattr(obj, "__name__"):
                    if obj.__name__.startswith(module_name):
                        graph.add_edge(m.__name__, obj.__name__)
                        _build_deps(obj)

        _build_deps(mod)
        return {"nodes": list(graph.nodes), "edges": list(graph.edges)}
