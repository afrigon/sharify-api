# -*- coding: utf-8 -*-

from ..abstract_version_change import AbstractVersionChange
from ...domain.types import Track


class TrackExternalLinks(AbstractVersionChange):
    def description():
        return ''

    def api_resource_type():
        return Track

    def apply(data, **kwargs):
        try:
            data.url = data.externals[kwargs['target']]['url']
        except Exception:
            data.url = ''

        delattr(data, 'externals')

        return data
