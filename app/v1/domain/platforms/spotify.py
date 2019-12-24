# -*- coding: utf-8 -*-

import os
from base64 import b64encode
from .platform import Platform
from ....utils.date import now
from .errors import PlatformErrorType
from ...domain.types import Track, Album, Artist
from .types import PlatformType
from ..link_type import LinkType
from ....utils import get

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
            self._update_status(PlatformErrorType.AUTH_REFRESH.value)
            return None, 0

    @Platform._authenticated
    def get_track(self, track_id: str):
        r = self.session.get(f'{HOST}/tracks/{track_id}')

        try:
            data = r.json()

            isrc = data['external_ids']['isrc']
            title = data['name']
            album = data['album']['name']
            artist = get(data, 'artists', 0, 'name', default='Artist Name')
            genres = []

            images = data['album']['images']
            for image in images:
                if image['height'] == 640:
                    image_url = image['url']
            image_url = image_url or images[0]['url']

            audio_url = data['preview_url']
            url = data['external_urls']['spotify']

            track = Track(isrc, title, album, artist, image_url, audio_url, genres)
            track.add_external(PlatformType.SPOTIFY, track_id, url)

            self._update_status(r.status_code)

            return track
        except Exception as e:
            print(e)
            self._update_status(PlatformErrorType.PARSING.value)
            return None

    @Platform._authenticated
    def get_album(self, album_id: str):
        r = self.session.get(f'{HOST}/albums/{album_id}')

        try:
            data = r.json()

            genres = data['genres']
            url = data['external_urls']['spotify']

            track_id = get(data, 'tracks', 'items', 0, 'id', default=None)
            if not track_id:
                return None

            track = self.get_track(track_id)

            album = Album(track.isrc,
                          track.album,
                          track.artist,
                          track.image_url,
                          track.audio_url,
                          genres)
            album.add_external(PlatformType.SPOTIFY, album_id, url)

            self._update_status(r.status_code)

            return album
        except Exception as e:
            print(e)
            self._update_status(PlatformErrorType.PARSING.value)
            return None

    @Platform._authenticated
    def get_artist(self, artist_id: str):
        artistr = self.session.get(f'{HOST}/artists/{artist_id}')
        trackr = self.session.get(f'{HOST}/artists/{artist_id}/top-tracks?country=us')

        try:
            data = artistr.json()

            name = data['name']
            genres = data['genres']
            url = data['external_urls']['spotify']

            images = data['images']
            for image in images:
                if image['height'] == 640:
                    image_url = image['url']
            image_url = image_url or images[0]['url']

            tracks = trackr.json()
            tracks = tracks['tracks'][0]

            isrc = tracks['external_ids']['isrc']
            audio_url = tracks['preview_url']

            artist = Artist(isrc, name, image_url, audio_url, genres)
            artist.add_external(PlatformType.SPOTIFY, artist_id, url)

            self._update_status(artistr.status_code)

            return artist
        except Exception as e:
            print(e)
            self._update_status(PlatformErrorType.PARSING.value)
            return None

    @Platform._authenticated
    def get_external(self, isrc: str, link_type: LinkType = LinkType.TRACK):
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
            track = get(data, 'tracks', 'items', 0, default=None)

            if not track:
                return None

            if link_type == LinkType.TRACK:
                item = track
            elif link_type == LinkType.ALBUM:
                item = track['album']
            elif link_type == LinkType.ARTIST:
                item = track['artists'][0]

            external = {
                'item_id': item['id'],
                'url': item['external_urls']['spotify']
            }

            self._update_status(r.status_code)

            return external
        except Exception as e:
            print(f'spotify.get_external: {e}')
            self._update_status(PlatformErrorType.PARSING.value)
            return None
