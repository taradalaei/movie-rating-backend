from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.controller.movies import router as movies_router

app = FastAPI(title="Movie Rating System")

app.include_router(movies_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "failure",
            "error": {"code": exc.status_code, "message": str(exc.detail)},
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Guide expects a single message string; use the first validation error message when available.
    msg = "Validation Error"
    errors = exc.errors()
    if errors:
        msg = errors[0].get("msg", msg)

    return JSONResponse(
        status_code=422,
        content={
            "status": "failure",
            "error": {"code": 422, "message": msg},
        },
    )


@app.get("/health")
def health():
    return {"status": "ok"}
