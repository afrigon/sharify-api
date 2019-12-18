# -*- coding: utf-8 -*-

import abc
import functools
from ..utils.date import now
from ..utils import Singleton


class Platform(Singleton):  # pragma: no cover
    def __init__(self):
        self.access_token = None
        self.expires_at = 0

    def _authenticate(self):
        self.access_token, self.expires_at = self._get_access_token()

        headers = {} if self.access_token is None else {
            'Authorization': f'Bearer {self.access_token}'
        }

        self.session.headers.update(headers)

    def _authenticated(f):
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            if self.access_token is None or self.expires_at < now(30):
                self._authenticate()

            return f(self, *args, **kwargs)

        return wrapper

    @abc.abstractmethod
    def _get_access_token(self):
        return None

    @abc.abstractmethod
    def get_track(self, track_id: str):
        return None

    @abc.abstractmethod
    def get_url(self, isrc: str):
        return None
