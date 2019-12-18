# -*- coding: utf-8 -*-

from urllib.parse import urlparse
from ..platforms import PlatformType

SPOTIFY_HOSTS = ['open.spotify.com', 'api.spotify.com']
APPLE_MUSIC_HOSTS = ['music.apple.com']


def parse_url(url: str):
    u = urlparse(url)
    if u.netloc in SPOTIFY_HOSTS:
        # TODO: check type (track, album, artist)
        parts = u.path.split('/')
        if len(parts) < 2:
            return None, PlatformType.SPOTIFY
        return parts[2], PlatformType.SPOTIFY
    elif u.netloc in APPLE_MUSIC_HOSTS:
        return 'apple-yo', PlatformType.SPOTIFY
    else:
        return None, None


def parse_platform(platform: str):
    if platform == PlatformType.SPOTIFY.value:
        return PlatformType.SPOTIFY
    elif platform == PlatformType.APPLE_MUSIC.value:
        return PlatformType.APPLE_MUSIC
    else:
        return None
