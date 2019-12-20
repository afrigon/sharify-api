# -*- coding: utf-8 -*-

from unittest.mock import Mock, patch
from threading import Thread
from . import MockPlatform

AUTHENTICATION_COUNT = 10


def test_whenTokenIsSetAndNotExpired_thenIsAuthenticated():
    platform = MockPlatform()

    platform._authenticate()

    assert platform._is_authenticated()


def test_whenTokenIsNotSet_thenIsNotAuthenticated():
    platform = MockPlatform()

    platform._authenticate()
    platform.access_token = None

    assert not platform._is_authenticated()


def test_whenTokenIsExpired_thenIsNotAuthenticated():
    platform = MockPlatform()

    platform._authenticate()
    platform.expires_at = 0

    assert not platform._is_authenticated()


def test_whenAuthenticatingManyTimesSimultaniously_thenIsAuthenticatedOnce():
    platform = MockPlatform()

    access_token_setter = Mock(wraps=MockPlatform.access_token.fset)
    mock = MockPlatform.access_token.setter(access_token_setter)
    with patch.object(MockPlatform, 'access_token', mock):
        def task(p):
            p._authenticate()

        threads = []
        for _ in range(AUTHENTICATION_COUNT):
            t = Thread(target=task, args=[platform], group=None)
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

        access_token_setter.assert_called_once()
