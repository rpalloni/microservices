# https://dev.to/visini/implementing-fastapi-services-abstraction-and-separation-of-concerns-218p

# cd microservices
# uvicorn services.main:app
# http://0.0.0.0:8000/docs

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from services.routers import foo
from services.config.database import create_tables
from services.utils.request_exceptions import http_exception_handler,request_validation_exception_handler
from services.utils.app_exceptions import AppExceptionCase, app_exception_handler

create_tables()


app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


app.include_router(foo.router)
