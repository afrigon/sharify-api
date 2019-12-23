# -*- coding: utf-8 -*-

from fastapi.routing import APIRouter
from fastapi import Header, HTTPException
from .versioning import VersionChanges
from .domain.platforms import PlatformType
from .domain.link_type import LinkType
from .services import TranslationService, HealthService
from .domain.platforms import PlatformFactory

router = APIRouter()

platformFactory = PlatformFactory()
translationService = TranslationService(platformFactory)
healthService = HealthService(platformFactory)


@router.get('/translate/{platform}/{link_type}/{link_id}')
def translate(link_id: str,
              link_type: LinkType,
              platform: PlatformType,
              target: PlatformType = None,
              sharify_version: str = Header(None)):

    if target is None:
        # fetch all
        pass

    # wrap this in a try except with domain errors, then throw actual httpexception from here
    item = translationService.translate(link_id,
                                        link_type,
                                        platform,
                                        target)

    #if item is None:
    #    raise HTTPException(404, f'{link_id} does not exist on the {platform.value} platform')

    #if url is None:
    #    raise HTTPException(404, f'Could not find matching ISRC on the {target.value} platform')

    #item.url = url

    return VersionChanges.instance().apply(item,
                                           until=sharify_version,
                                           target=target.value)


@router.get('/health', tags=['Monitoring'])
async def health(sharify_version: str = Header(None)):
    status = healthService.status()
    print(status)

    return VersionChanges.instance().apply(status,
                                           until=sharify_version)
