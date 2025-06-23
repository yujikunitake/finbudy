from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routers.users import users_router

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(users_router)

    return app

app = create_app()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail if isinstance(exc.detail, str) else exc.detail.get("message", "Erro inesperado."),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]
    field = ".".join(str(part) for part in error["loc"] if part != "body")
    message = error["msg"]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": f"Field '{field}': {message}"
        }
    )
