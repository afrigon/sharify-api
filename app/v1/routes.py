from fastapi.routing import APIRouter
from fastapi import Header, HTTPException
from .versioning import VersionChanges
from .domain.platforms import PlatformType
from .domain.link_type import LinkType
from .services import TranslationService, HealthService, ParsingService
from .domain.platforms import PlatformFactory
from .domain.errors import ItemNotFoundError, InvalidURLError

router = APIRouter()

platformFactory = PlatformFactory()
translationService = TranslationService(platformFactory)
healthService = HealthService(platformFactory)
parsingService = ParsingService()


@router.get('/translate/{platform}/{link_type}/{link_id}', tags=['Translation'])
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


@router.get('/translate', tags=['Translation'])
def parse_translate(url: str,
                    target: PlatformType = None,
                    sharify_version: str = Header(None)):
    try:
        query = parsingService.parse(url)
    except InvalidURLError:
        return HTTPException(404, 'could not parse url into a valid LinkQuery object')

    link_type = LinkType(query.type)
    platform = PlatformType(query.platform)

    try:
        item = translationService.translate(query.id,
                                            link_type,
                                            platform,
                                            target)
    except ItemNotFoundError:
        raise HTTPException(404, f'could not find {query.type} {query.id} on {query.platform}')

    return VersionChanges.instance().apply(item,
                                           until=sharify_version,
                                           target=target)


@router.get('/parse', tags=['Parsing'])
async def parse(url: str, sharify_version: str = Header(None)):
    try:
        query = parsingService.parse(url)
    except InvalidURLError:
        return HTTPException(404, 'could not parse url into a valid LinkQuery object')

    return VersionChanges.instance().apply(query,
                                           until=sharify_version)


@router.get('/health', tags=['Monitoring'])
async def health(sharify_version: str = Header(None)):
    status = healthService.status()

    return VersionChanges.instance().apply(status,
                                           until=sharify_version)
