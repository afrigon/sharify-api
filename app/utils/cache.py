import os
import pickle
import redis

from ..v1.domain.types import SharifyObject
from ..v1.domain.platforms.types import PlatformType
from ..v1.domain.link_type import LinkType
from ..utils import Singleton


class Cache(Singleton):
    def init(self):
        host = os.environ.get('REDIS_HOST', 'localhost')
        port = os.environ.get('REDIS_PORT', 6379)
        self.r = redis.StrictRedis(host=host, port=port, db=0)
        self.enabled = True

        try:
            self.r.ping()
        except Exception:
            print(f'could not connect to redis://{host}:{port}/0, disableling caching')
            self.enabled = False

    def set(self,
            key: str,
            platform: PlatformType,
            link_type: LinkType,
            obj: SharifyObject):
        if not self.enabled:
            return

        try:
            key = f'{platform.value}/{link_type.value}/{key}'
            pickled = pickle.dumps(obj)
            self.r.set(key, pickled)
        except Exception:
            pass

    def get(self,
            key: str,
            platform: PlatformType,
            link_type: LinkType):
        if not self.enabled:
            return None

        try:
            key = f'{platform.value}/{link_type.value}/{key}'
            obj = self.r.get(key)
            return pickle.loads(obj)
        except Exception:
            return None
