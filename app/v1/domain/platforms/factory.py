from ..platforms import PlatformType, SpotifyPlatform, AppleMusicPlatform


class PlatformFactory:
    def create(self, type: PlatformType):
        if type == PlatformType.SPOTIFY:
            return SpotifyPlatform.instance()
        elif type == PlatformType.APPLE_MUSIC:
            return AppleMusicPlatform.instance()
