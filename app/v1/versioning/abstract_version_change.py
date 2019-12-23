# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from ..domain.types import SharifyObject


class AbstractVersionChange(ABC):
    @property
    @abstractmethod
    def description():
        pass

    @property
    @abstractmethod
    def api_resource_type():
        pass

    @abstractmethod
    def apply(resource: SharifyObject, **kwargs):
        pass
