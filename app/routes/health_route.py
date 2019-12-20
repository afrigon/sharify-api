# -*- coding: utf-8 -*-

from .route import Route


class HealthRoute(Route):
    def __init__(self, service):
        self.service = service

    def get_name(self):
        return 'translation'

    def register(self, app):
        app.add_api_route('/health',
                          self.status,
                          methods=['GET'],
                          name='health',
                          tags=['Monitoring'])

    def status(self):
        return self.service.status()