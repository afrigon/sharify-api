from time import sleep
from app.platforms.platform import Platform
from app.utils.date import now


class MockPlatform(Platform):
    def _get_access_token(self):
        sleep(0.1)
        return "SOME-TOKEN", now(3600)
