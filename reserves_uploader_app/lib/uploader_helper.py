import logging, pprint

import requests
from django.conf import settings
from django.core.cache import cache


log = logging.getLogger(__name__)


def build_uploader_GET_context() -> dict:
    """ Builds context for the uploader page.
        Called by views.uploader() """
    log.debug( 'starting' )
    context = {}
    pattern_header_html: str = prep_pattern_header_html()
    context['pattern_header'] = pattern_header_html
    log.debug( f'context, ``{pprint.pformat(context)[0:500]}``' )
    return context


def prep_pattern_header_html() -> str:
    """ Builds pattern-header html.
        Called by build_uploader_GET_context() """
    log.debug( 'starting' )
    cache_key = 'pattern_header'
    header_html = cache.get( cache_key, None )
    if header_html:
        log.debug( 'header in cache' )
    else:
        log.debug( 'header not in cache' )
        r = requests.get( settings.PATTERN_LIB_HEADER_URL )
        header_html: str = r.content.decode( 'utf8' )
        cache.set( cache_key, header_html, settings.PATTERN_LIB_CACHE_TIMEOUT )
    log.debug( f'header_html, ``{header_html[0:500]}``' )
    return header_html