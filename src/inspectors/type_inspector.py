from typing import Any, Dict, Optional
from src.inspectors.class_inspector import ClassInspector

class TypeHierarchyInspector:
    @staticmethod
    def get_type_hierarchy(qualified_name: str, environment: Optional[str] = None) -> Dict[str, Any]:
        """Provides type hierarchy for a given class."""
        return ClassInspector.type_hierarchy(qualified_name, environment)
