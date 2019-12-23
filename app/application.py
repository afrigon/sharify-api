# -*- coding: utf-8 -*-

from fastapi import FastAPI
from . import __version__
from .routes import router


class ApplicationFactory:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def create(self, debug=False):
        app = FastAPI(title=self.title,
                      description=self.description,
                      version=__version__,
                      debug=debug)

        app.include_router(router)

        return app
