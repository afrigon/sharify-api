# -*- coding: utf-8 -*-

from . import Router
from . import TranslationRoute
from ..services import TranslationService
from ..platforms import PlatformFactory


class RouterFactory:
    def create(self):
        translation = TranslationRoute(TranslationService(PlatformFactory()))

        return Router(translation)
