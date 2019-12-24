# -*- coding: utf-8 -*-

from fastapi.routing import APIRouter
from fastapi import Header, HTTPException
from .versioning import VersionChanges
from .domain.platforms import PlatformType
from .domain.link_type import LinkType
from .services import TranslationService, HealthService
from .domain.platforms import PlatformFactory
from .domain.errors import ItemNotFoundError

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
    try:
        item = translationService.translate(link_id,
                                            link_type,
                                            platform,
                                            target)
    except ItemNotFoundError:
        raise HTTPException(404, f'could not find {link_type.value} {link_id} on {platform.value}')

    return VersionChanges.instance().apply(item,
                                           until=sharify_version,
                                           target=target)


@router.get('/health', tags=['Monitoring'])
async def health(sharify_version: str = Header(None)):
    status = healthService.status()
    print(status)

    return VersionChanges.instance().apply(status,
                                           until=sharify_version)
