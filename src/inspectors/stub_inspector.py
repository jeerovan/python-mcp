import os
from typing import Any, Dict, Optional

class StubInspector:
    @staticmethod
    def stub_info(file_path: str) -> Dict[str, Any]:
        if not file_path.endswith(".pyi"):
            raise ValueError("File is not a stub (.pyi)")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Stub file not found: {file_path}")
        
        with open(file_path, "r") as f:
            content = f.read()
            
        return {
            "path": file_path,
            "content": content,
            "size": len(content)
        }
