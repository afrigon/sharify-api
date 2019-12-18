# -*- coding: utf-8 -*-

from .route import Route
from ..utils.parser import parse_platform
from fastapi import HTTPException


class TranslationRoute(Route):
    def __init__(self, service):
        self.service = service

    def get_name(self):
        return 'translation'

    def register(self, app):
        app.add_api_route('/translate',
                          self.get,
                          methods=['GET'],
                          name='translate',
                          tags=['Translation'])

    def get(self, track_id: str, source: str, destination: str):
        src_platform = parse_platform(source)
        if src_platform is None:
            raise HTTPException(400, 'could not parse source platform')

        dst_platform = parse_platform(destination)
        if dst_platform is None:
            raise HTTPException(400, 'could not parse destination platform')

        track, url = self.service.translate(track_id,
                                            src_platform,
                                            dst_platform)

        if track is None:
            raise HTTPException(404, f'{track_id} does not exist on the {source} platform')

        if url is None:
            raise HTTPException(404, f'Could not find matching ISRC on the {destination} platform')

        track.url = url
        return track


