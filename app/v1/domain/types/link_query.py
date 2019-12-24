# -*- coding: utf-8 -*-

from .sharify_object import SharifyObject


class LinkQuery(SharifyObject):
    def __init__(self, 
                 link_id: str,
                 link_type: str,
                 platform: str):
        self.id = link_id
        self.type = link_type
        self.platform = platform
