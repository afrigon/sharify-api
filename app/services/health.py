# -*- coding: utf-8 -*-

from ..platforms import PlatformFactory, PlatformType


class HealthService:
    def __init__(self, platformFactory: PlatformFactory):
        self.platformFactory = platformFactory

    def status(self):
        status = {}

        for type in PlatformType:
            platform = self.platformFactory.create(type)
            status[type.value] = platform.status

        return status
