# -*- coding: utf-8 -*-

from ..domain.platforms import PlatformFactory, PlatformType
from ..domain.link_type import LinkType
from ..domain.errors import ItemNotFoundError
from ...utils.cache import Cache


class TranslationService:
    def __init__(self, platformFactory: PlatformFactory):
        self.platformFactory = platformFactory

    def translate(self,
                  link_id: str,
                  link_type: LinkType,
                  src: PlatformType,
                  dst: PlatformType):
        item = Cache.instance().get(link_id, src, link_type)

        if not item:
            s = self.platformFactory.create(src)

            if link_type == LinkType.TRACK:
                item = s.get_track(link_id)
            elif link_type == LinkType.ALBUM:
                item = s.get_album(link_id)
            elif link_type == LinkType.ARTIST:
                item = s.get_artist(link_id)

        if not item:
            raise ItemNotFoundError()

        if not dst:
            for platform in PlatformType:
                if platform == src or item.externals.get(platform.value):
                    continue

                d = self.platformFactory.create(platform)
                external = d.get_external(item.isrc, link_type=link_type)

                if external:
                    item.add_external(platform, **external)
        else:
            if not item.externals.get(dst.value):
                d = self.platformFactory.create(dst)
                external = d.get_external(item.isrc, link_type=link_type)

                if external:
                    item.add_external(dst, **external)

        Cache.instance().set(link_id, src, link_type, item)

        return item
