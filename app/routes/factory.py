# -*- coding: utf-8 -*-

from . import Router
from . import TranslationRoute, HealthRoute
from ..services import TranslationService, HealthService
from ..platforms import PlatformFactory


class RouterFactory:
    def create(self):
        platformFactory = PlatformFactory()

        translation = TranslationRoute(TranslationService(platformFactory))
        health = HealthRoute(HealthService(platformFactory))

        return Router(translation, health)
