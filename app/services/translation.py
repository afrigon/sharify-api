# -*- coding: utf-8 -*-

from ..platforms import PlatformFactory, PlatformType


class TranslationService:
    def __init__(self, platformFactory: PlatformFactory):
        self.platformFactory = platformFactory

    def translate(self,
                  track_id: str,
                  src: PlatformType,
                  dst: PlatformType):
        s = self.platformFactory.create(src)
        d = self.platformFactory.create(dst)

        track = s.get_track(track_id)
        if track is None:
            return None, None

        url = d.get_url(track.isrc)

        return track, url
