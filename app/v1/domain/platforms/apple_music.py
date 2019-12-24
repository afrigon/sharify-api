# -*- coding: utf-8 -*-

import os
import jwt
from .platform import Platform
from ....utils.date import now
from .errors import PlatformErrorType
from ..link_type import LinkType
from ..types import Track, Album, Artist
from .types import PlatformType
from ....utils import get
from bs4 import BeautifulSoup

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

            isrc = data['isrc']
            title = data['name']
            album = data['albumName']
            artist = data['artistName']
            genres = data['genreNames']

            image_url = data['artwork']['url']
            image_url = image_url.replace('{w}x{h}', f'{IMG_SIZE}x{IMG_SIZE}')

            audio_url = get(data, 'previews', 0, 'url', default=None)

            url = data['url']

            track = Track(isrc, title, album, artist, image_url, audio_url, genres)
            track.add_external(PlatformType.APPLE_MUSIC, track_id, url)

            self._update_status(r.status_code)

            return track
        except Exception:
            self._update_status(PlatformErrorType.PARSING.value)
            return None

    @Platform._authenticated
    def get_album(self, album_id: str):
        r = self.session.get(f'{HOST}/catalog/{REGION}/albums/{album_id}')

        try:
            data = r.json()
            data = data['data'][0]

            title = data['attributes']['name']
            artist = data['attributes']['artistName']
            genres = data['attributes']['genreNames']
            url = data['attributes']['url']

            track = get(data,
                        'relationships',
                        'tracks',
                        'data',
                        0,
                        'attributes',
                        default=None)
            if not track:
                return None

            isrc = track['isrc']

            image_url = track['artwork']['url']
            image_url = image_url.replace('{w}x{h}', f'{IMG_SIZE}x{IMG_SIZE}')

            audio_url = get(track, 'previews', 0, 'url', default=None)

            album = Album(isrc,
                          title,
                          artist,
                          image_url,
                          audio_url,
                          genres)
            album.add_external(PlatformType.APPLE_MUSIC, album_id, url)

            self._update_status(r.status_code)

            return album
        except Exception as e:
            print(e)
            self._update_status(PlatformErrorType.PARSING.value)
            return None


    @Platform._authenticated
    def get_artist(self, artist_id: str):
        r = self.session.get(f'{HOST}/catalog/{REGION}/artists/{artist_id}')

        try:
            data = r.json()
            data = data['data'][0]

            name = data['attributes']['name']
            genres = data['attributes']['genreNames']
            url = data['attributes']['url']

            image_url = self.get_artist_image(url)

            album_id = get(data,
                           'relationships',
                           'albums',
                           'data',
                           0,
                           'id',
                           default=None)
            if not album_id:
                return None

            album = self.get_album(album_id)

            artist = Artist(album.isrc,
                            name,
                            image_url,
                            album.audio_url,
                            genres)
            artist.add_external(PlatformType.APPLE_MUSIC, artist_id, url)

            self._update_status(r.status_code)

            return artist
        except Exception as e:
            print(e)
            self._update_status(PlatformErrorType.PARSING.value)
            return None

    def get_artist_image(self, url: str):
        r = self.session.get(url)
        try:
            data = BeautifulSoup(r.text, 'html.parser')
            data = data.find(class_='we-artwork--artist-header-profile')
            data = data.find(class_='we-artwork__image')

            image_url = data['src']
            image_url = image_url[:image_url.rindex('/')]
            image_url = f'{image_url}/{IMG_SIZE}x{IMG_SIZE}-999.jpg'

            return image_url
        except Exception:
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
            track = data['data'][0]

            self._update_status(r.status_code)

            if link_type == LinkType.TRACK:
                return {
                    'item_id': track['id'],
                    'url': track['attributes']['url']
                }

            if link_type == LinkType.ALBUM:
                album_id = track['relationships']['albums']['data'][0]['id']
                item = self.get_album(album_id)
            elif link_type == LinkType.ARTIST:
                artist_id = track['relationships']['artists']['data'][0]['id']
                item = self.get_artist(artist_id)

            external = {
                'item_id': item.externals['apple-music']['id'],
                'url': item.externals['apple-music']['url'],
            }

            return external
        except Exception as e:
            print(e)
            self._update_status(PlatformErrorType.PARSING.value)
            return None
