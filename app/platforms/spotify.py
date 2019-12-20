# -*- coding: utf-8 -*-

import os
from base64 import b64encode
from .platform import Platform
from ..track import Track
from ..utils.date import now
from ..errors import ErrorType

AUTH_URL = 'https://accounts.spotify.com/api/token'
VERSION = 'v1'
HOST = f'https://api.spotify.com/{VERSION}'


class SpotifyPlatform(Platform):
    def __init__(self):
        Platform.__init__(self)
        self.client_id = os.environ['SPOTIFY_CLIENT_ID']
        self.client_secret = os.environ['SPOTIFY_CLIENT_SECRET']

    def _get_access_token(self):
        creds = f'{self.client_id}:{self.client_secret}'
        creds_token = b64encode(creds.encode('utf-8')).decode('utf-8')

        headers = {'Authorization': f'Basic {creds_token}'}
        body = {'grant_type': 'client_credentials'}

        r = self.session.post(AUTH_URL, headers=headers, data=body)

        try:
            data = r.json()

            expires_in = int(data.get('expires_in') or 0)
            expires_at = now(expires_in)

            token = data.get('access_token') or None

            return token, expires_at
        except Exception:
            return None, 0

    @Platform._authenticated
    def get_track(self, track_id: str):
        r = self.session.get(f'{HOST}/tracks/{track_id}')

        try:
            data = r.json()

            title = data['name']
            author = data['artists'][0]['name']
            album = data['album']['name']
            isrc = data['external_ids']['isrc']

            images = data['album']['images']
            for image in images:
                if image['height'] == 640:
                    image_url = image['url']
            image_url = image_url or images[0]['url']

            track = Track(title,
                          author,
                          album,
                          isrc,
                          image_url)
            track.add_id(track_id, 'spotify')

            self._update_status(r.status_code)

            return track
        except Exception:
            self._update_status(ErrorType.PARSING)
            return None

    @Platform._authenticated
    def get_url(self, isrc: str):
        if isrc is None:
            return None

        params = {
            'q': f'isrc:{isrc}',
            'type': 'track',
            'limit': 1
        }

        r = self.session.get(f'{HOST}/search', params=params)

        try:
            data = r.json()
            tracks = data['tracks']['items']

            if len(tracks) != 1:
                return None

            url = tracks[0]['external_urls']['spotify']

            self._update_status(r.status_code)

            return url
        except Exception:
            self._update_status(ErrorType.PARSING)
            return None
