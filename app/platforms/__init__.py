# -*- coding: utf-8 -*-

from enum import Enum

from .apple_music import AppleMusicPlatform  # noqa: F401
from .spotify import SpotifyPlatform  # noqa: F401


class PlatformType(Enum):
    SPOTIFY = 'spotify'
    APPLE_MUSIC = 'apple-music'


from .factory import PlatformFactory  # noqa: F401
