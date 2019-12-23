# -*- coding: utf-8 -*-

from fastapi.routing import APIRouter
from . import v1

router = APIRouter()
router.include_router(v1.router)
