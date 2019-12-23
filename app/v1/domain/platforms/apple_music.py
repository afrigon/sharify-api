# -*- coding: utf-8 -*-

import os
import jwt
from .platform import Platform
from ....utils.date import now
from .errors import PlatformErrorType
from ..link_type import LinkType
from ..types import Track
from .types import PlatformType

VERSION = 'v1'
REGION = 'us'
HOST = f'https://api.music.apple.com/{VERSION}'
TOKEN_TTL = 3600
IMG_SIZE = 640


class AppleMusicPlatform(Platform):
    def __init__(self):
        Platform.__init__(self)
        self.kid = os.environ['APPLE_KID']
        self.team_id = os.environ['APPLE_TEAM_ID']
        self.key = os.environ['APPLE_KEY']

    def _get_access_token(self):
        expires_at = now(TOKEN_TTL)

        headers = {
            'kid': self.kid
        }

        payload = {
            'iss': self.team_id,
            'iat': now(),
            'exp': expires_at
        }

        token = jwt.encode(payload,
                           self.key,
                           algorithm='ES256',
                           headers=headers)
        token = token.decode('utf-8')

        return token, expires_at

    @Platform._authenticated
    def get_track(self, track_id: str):
        r = self.session.get(f'{HOST}/catalog/{REGION}/songs/{track_id}')

        try:
            data = r.json()
            data = data['data'][0]['attributes']

            title = data['name']
            album = data['albumName']
            artist = data['artistName']
            isrc = data['isrc']
            image_url = data['artwork']['url']
            image_url = image_url.replace('{w}x{h}', f'{IMG_SIZE}x{IMG_SIZE}')
            audio_url = data['previews'][0]['url']
            url = data['url']

            track = Track(isrc, title, album, artist, image_url, audio_url)
            track.add_external(PlatformType.APPLE_MUSIC, track_id, url)

            self._update_status(r.status_code)

            return track
        except Exception:
            self._update_status(PlatformErrorType.PARSING.value)
            return None

    @Platform._authenticated
    def get_external(self, isrc: str, link_type: LinkType = LinkType.TRACK):
        if isrc is None:
            return None

        params = {
            'filter[isrc]': isrc
        }

        r = self.session.get(f'{HOST}/catalog/{REGION}/songs', params=params)

        try:
            data = r.json()
            data = data['data'][0]

            external = {
                'item_id': data['id'],
                'url': data['attributes']['url']
            }

            self._update_status(r.status_code)

            return external
        except Exception:
            self._update_status(PlatformErrorType.PARSING.value)
            return None
