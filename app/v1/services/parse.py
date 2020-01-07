import re
from ..domain.errors import InvalidURLError
from ..domain.types import LinkQuery
from ..domain.platforms.types import PlatformType
from ..domain.link_type import LinkType


class ParsingService:
    def parse(self, url: str):
        # spotify:track:6voo8x5qmBvabjEOxPHesp
        m = re.search(r'spotify:(//)?(?P<link_type>album|track|artist):(?P<link_id>\w*)', url)
        if m:
            return LinkQuery(m.group('link_id'),
                             m.group('link_type'),
                             PlatformType.SPOTIFY.value)

        # https://open.spotify.com/track/6voo8x5qmBvabjEOxPHesp
        m = re.search(r'https://(api|open)\.spotify\.com/(?P<link_type>album|track|artist)/(?P<link_id>\w*)', url)
        if m:
            return LinkQuery(m.group('link_id'),
                             m.group('link_type'),
                             PlatformType.SPOTIFY.value)

        # https://music.apple.com/us/album/where-will-we-go-acoustic/1490944379?i=1490944380
        m = re.search(r'https://music\.apple\.com/(([a-z]{2})/)?album/(([\w-]*)/)?(\d*)\?(\w*=\w*&)*i=(?P<link_id>\d+)', url)
        if m:
            return LinkQuery(m.group('link_id'),
                             LinkType.TRACK.value,
                             PlatformType.APPLE_MUSIC.value)

        # https://music.apple.com/us/album/where-will-we-go-acoustic/1490944379
        m = re.search(r'https://music\.apple\.com/(([a-z]{2})/)?album/(([\w-]*)/)?(?P<link_id>\d*)', url)
        if m:
            return LinkQuery(m.group('link_id'),
                             LinkType.ALBUM.value,
                             PlatformType.APPLE_MUSIC.value)

        # https://music.apple.com/us/artist/grant/1423400231
        m = re.search(r'https://music\.apple\.com/(([a-z]{2})/)?artist/(([\w-]*)/)?(?P<link_id>\d*)', url)
        if m:
            return LinkQuery(m.group('link_id'),
                             LinkType.ARTIST.value,
                             PlatformType.APPLE_MUSIC.value)

        raise InvalidURLError()
