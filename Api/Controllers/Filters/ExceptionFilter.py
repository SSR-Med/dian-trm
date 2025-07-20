from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from Infrastructure.Exceptions.BadRequestException import BadRequestException

def register_custom_exception_handlers(app: FastAPI):
    """
    Registra los manejadores de excepciones personalizadas en la aplicación FastAPI.
    """

    @app.exception_handler(BadRequestException)
    async def bad_request_exception_handler(request: Request, exc: BadRequestException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": exc.message, "detail": exc.detail}
        )
