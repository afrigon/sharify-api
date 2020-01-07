from . import changes  # noqa: F401
from ...utils.singleton import Singleton
from ..domain.types import SharifyObject
from collections import OrderedDict


class VersionChanges(Singleton):
    VERSIONS = {
        '2019-12-23': [
            changes.TrackExternalLinks
        ]
    }

    def apply(self, data: SharifyObject, until: str = None, **kwargs):
        if not until:
            return data

        dates = VersionChanges.VERSIONS.keys()

        for date in dates:
            if date < until:
                break

            for change in VersionChanges.VERSIONS[date]:
                if isinstance(data, change.api_resource_type()):
                    change.apply(data, **kwargs)

        return data


VersionChanges.VERSIONS = OrderedDict(sorted(
    VersionChanges.VERSIONS.items(),
    key=lambda t: t[0],
    reverse=True)
)
