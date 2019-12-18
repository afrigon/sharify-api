# -*- coding: utf-8 -*-

from app.routes import RouterFactory


def test_whenCreatingRouter_thenTranslationRouteIsRegistered(app):
    router = RouterFactory().create()
    assert 'translation' in router.routes
