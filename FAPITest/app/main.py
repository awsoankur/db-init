from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts,user,auth,votes
from .config import settings
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc:HTTPException):
    d = {
        "error": {
                'code': exc.status_code,
                'message': exc.detail,
                'details': {},
                'validation_errors': [],
                'retryable': False
            }
    }
    return JSONResponse(content=jsonable_encoder(d),status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc:RequestValidationError):
    d = {
        "error": {
                'code': 422,
                'message': "Invalid Request Body",
                'details': "",
                'validation_errors': exc.errors() ,
                'retryable': False
            }
    }
    return JSONResponse(content=jsonable_encoder(d),status_code=422)

    # return await request_validation_exception_handler(request, exc)


app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
async def root():
    return {"message":"Hiiiiiiiiiiin more"}