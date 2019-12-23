# -*- coding: utf-8 -*-

from ..domain.platforms import PlatformFactory, PlatformType
from ..domain.link_type import LinkType


class TranslationService:
    def __init__(self, platformFactory: PlatformFactory):
        self.platformFactory = platformFactory

    def translate(self,
                  link_id: str,
                  link_type: LinkType,
                  src: PlatformType,
                  dst: PlatformType):
        s = self.platformFactory.create(src)
        d = self.platformFactory.create(dst)

        if link_type == LinkType.TRACK:
            item = s.get_track(link_id)
        #elif link_type == LinkType.ALBUM:
        #    item = s.get_album(link_id)
        #elif link_type == LinkType.ARTIST:
        #    item = s.get_artist(link_id)

        if item is None:
            # TODO: replace with an exception
            return None

        external = d.get_external(item.isrc, link_type=link_type)
        if external:
            item.add_external(dst, **external)

        return item
