import logging, pprint

import requests
from django.conf import settings
from django.core.cache import cache


log = logging.getLogger(__name__)


def build_uploader_GET_context( session_message: str ) -> dict:
    """ Builds context for the uploader page.
        Called by views.uploader() """
    log.debug( f'session_message, ``{session_message}``' )
    context = {
        'error_msg': '',
        'success_msg': '',
        'pattern_header': '',
    }
    pattern_header_html: str = prep_pattern_header_html()
    context['pattern_header'] = pattern_header_html
    if 'success' in repr( session_message ):
        context['success_msg'] = session_message
        context['error_msg'] = ''
    elif 'error' in repr( session_message ):
        context['success_msg'] = ''
        context['error_msg'] = session_message
    log.debug( f'context for GET, ``{pprint.pformat(context)[0:500]}``' )
    # log.debug( f'context.keys(), ``{pprint.pformat(context.keys())}``' )
    log.debug( f'context["error_msg"], ``{context["error_msg"]}``' )
    log.debug( f'context["success_msg"], ``{context["success_msg"]}``' )
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