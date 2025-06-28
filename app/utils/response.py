from fastapi.responses import JSONResponse
from typing import Any


def success_response(data: Any, status_code: int = 200) -> JSONResponse:
    return JSONResponse(
        content={
            "status": "success",
            "data": data
            },
        status_code=status_code
    )

def error_response(message: str, status_code: int = 400, extra: dict | None = None) -> JSONResponse:
    content={
        "status": "error",
        "message": message
    }
    if extra:
        content.update(extra)
    return JSONResponse(
        status_code=status_code,
        content=content
    )
