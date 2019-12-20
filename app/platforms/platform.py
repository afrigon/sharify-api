# -*- coding: utf-8 -*-

import abc
import functools
import requests
from threading import Lock
from ..utils.date import now
from ..utils import Singleton
from ..errors import ErrorType


class Platform(Singleton):  # pragma: no cover
    def __init__(self):
        self.session = requests.Session()
        self.lock = Lock()
        self._access_token = None
        self.expires_at = 0
        self._status = 'no-status'

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    @property
    def status(self):
        return self._status

    def _update_status(self, status_code):
        if status_code == ErrorType.THROTTLED:
            self._status = 'trottled'
        elif status_code >= 400:
            self._status = f'unavailable (status_code)'
        else:
            self._status = 'available'

    def _is_authenticated(self):
        return self.access_token is not None and self.expires_at >= now(30)

    def _authenticate(self):
        self.lock.acquire()

        # if access_token was refreshed by another thread, return
        if self._is_authenticated():
            return self.lock.release()

        self.access_token, self.expires_at = self._get_access_token()

        self.lock.release()

        headers = {} if self.access_token is None else {
            'Authorization': f'Bearer {self.access_token}'
        }
        self.session.headers.update(headers)

    def _authenticated(f):
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            if not self._is_authenticated:
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
