# -*- coding: utf-8 -*-

from app.routes import RouterFactory


def test_whenCreatingRouter_thenTranslationRouteIsRegistered(app):
    router = RouterFactory().create()
    assert 'translation' in router.routes


def test_whenCreatingRouter_thenHealthRouteIsRegistered(app):
    router = RouterFactory().create()
    assert 'health' in router.routes
