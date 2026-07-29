from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ErrorDetails(BaseModel):
    type: str
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)


class MCPResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[ErrorDetails] = None


def success_response(data: Any = None) -> Dict[str, Any]:
    return MCPResponse(success=True, data=data).model_dump()


def error_response(error_type: str, message: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return MCPResponse(
        success=False,
        error=ErrorDetails(type=error_type, message=message, details=details or {})
    ).model_dump()
