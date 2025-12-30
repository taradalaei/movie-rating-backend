from pydantic import BaseModel
from typing import Any


class ErrorDetail(BaseModel):
    code: int
    message: str


class FailureResponse(BaseModel):
    status: str = "failure"
    error: ErrorDetail


class SuccessResponse(BaseModel):
    status: str = "success"
    data: Any
