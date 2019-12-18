# -*- coding: utf-8 -*-


class Track:
    def __init__(self,
                 title: str,
                 author: str,
                 album: str,
                 isrc: str,
                 image_url: str):
        self.title = title
        self.author = author
        self.album = album
        self.isrc = isrc
        self.image_url = image_url
        self.ids = {}
        self.url = None

    def add_id(self, track_id: str, platform: str):
        self.ids[platform] = track_id
