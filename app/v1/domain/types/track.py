# -*- coding: utf-8 -*-

from .sharify_object import SharifyObject


class Track(SharifyObject):
    def __init__(self, 
                 isrc: str,
                 title: str,
                 album: str,
                 artist: str,
                 image_url: str,
                 audio_url: str):
        self.isrc = isrc
        self.title = title
        self.album = album
        self.artist = artist
        self.image_url = image_url
        self.audio_url = audio_url
        self.externals = {}

    def add_external(self, platform, item_id: str = '', url: str = ''):
        self.externals[platform.value] = {
            'id': item_id,
            'url': url
        }
