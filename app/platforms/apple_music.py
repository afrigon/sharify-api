# -*- coding: utf-8 -*-

import os
import jwt
from .platform import Platform
from ..track import Track
from ..utils.date import now

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
            author = data['artistName']
            album = data['albumName']
            isrc = data['isrc']
            image_url = data['artwork']['url']
            image_url = image_url.replace('{w}x{h}', f'{IMG_SIZE}x{IMG_SIZE}')

            track = Track(title,
                          author,
                          album,
                          isrc,
                          image_url)
            track.add_id(track_id, 'apple-music')

            return track
        except Exception:
            return None

    @Platform._authenticated
    def get_url(self, isrc: str):
        if isrc is None:
            return None

        params = {
            'filter[isrc]': isrc
        }

        r = self.session.get(f'{HOST}/catalog/{REGION}/songs', params=params)

        try:
            data = r.json()
            return data['data'][0]['attributes']['url']
        except Exception:
            return None
