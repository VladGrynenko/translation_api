# from typing import Union

from fastapi import FastAPI

from api.handlers import translation


def create_app():
    print("I am in create app")
    app = FastAPI(docs_url="/")

    # here include routers
    app.include_router(translation.router)
    return app
