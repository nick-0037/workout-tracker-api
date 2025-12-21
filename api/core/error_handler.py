from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status
from api.core.exceptions import AppException
from fastapi.exceptions import RequestValidationError


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.code,
        content={"error": exc.message},
    )
    
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Invalid request format", "details": exc.errors()},
    )
    
    
