from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routers.users import users_router
from app.routers.transactions import transactions_router
from app.utils.response import error_response


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(users_router)
    app.include_router(transactions_router)

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
    errors = []

    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"] if loc != "body")
        message = err["msg"]
        errors.append({"field": field, "message": message})

    return error_response(
        message="Validation failed",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        extra={"errors": errors}
    )
